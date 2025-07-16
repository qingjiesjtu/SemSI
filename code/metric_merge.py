from openai import OpenAI
import json
import os
from utils import *
from tqdm import tqdm
import re


def get_prompt(prompt_file):
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read()


def get_dataset(input_file):
    dataset = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            dataset.append(json.loads(line))
    return dataset

def evaluate(datafilename,resume=True,refined=True):
    filename=datafilename[:-6]+"_label.jsonl"
    with open('IDs1000.txt', 'r') as file:
        IDs1000 = [int(line.strip()) for line in file]

    S_prompt = get_prompt('promptPrivacy.txt')
    R_prompt = get_prompt('promptHarmful.txt')
    I_prompt = get_prompt('promptMisinformation.txt')
    dataset = get_dataset(datafilename)
    IDsDone=[]
    if resume and os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                IDsDone.append(json.loads(line)["ID"])
    for data in tqdm(dataset):
        if data["ID"] not in IDs1000 or data["ID"] in IDsDone: continue
        # evaluate Sensitive identity attributes
        attempts = 0
        done = False
        while attempts < 1: # Enough to handle json format errors; necessary when temperature>0
            completion = client.chat.completions.create(
                temperature=0,
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": S_prompt + data['answer']}
                ]
            )
            response = completion.choices[0].message.content
            response = re.sub(r'```json|```', '', response)
            response = response.strip()

            try:
                parsed_dict = json.loads(response)
                data['ifS'] = parsed_dict['ifS']
                if parsed_dict['ifS'] == 'yes':
                    data['S'] = parsed_dict['S']
                    data['scoreS'] = parsed_dict['scoreS']
                done = True
                print('valid')
            except json.JSONDecodeError as e:
                print(f"error: {str(e)}, error answer: {response}")
                if 'error' in data:
                    data['error'].append(response)
                else:
                    data['error']=[response]

            attempts += 1
            if done:
                break

        # evaluate Reputation-harmful contents
        attempts = 0
        done = False
        while attempts < 1:
            completion = client.chat.completions.create(
                temperature=0,
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": R_prompt + data['answer']}
                ]
            )
            response = completion.choices[0].message.content
            response = re.sub(r'```json|```', '', response)
            response = response.strip()

            try:
                parsed_dict = json.loads(response)
                data['ifR'] = parsed_dict['ifR']
                if parsed_dict['ifR'] == 'yes':
                    data['R'] = parsed_dict['R']
                    data['scoreR'] = parsed_dict['scoreR']
                done = True
                print('valid')
            except json.JSONDecodeError as e:
                print(f"error: {str(e)}, error answer: {response}")
                if 'error' in data:
                    data['error'].append(response)
                else:
                    data['error']=[response]
            
            attempts += 1
            if done:
                break
        
        # evaluate Incorrect hazardous information
        attempts = 0
        done = False
        while attempts < 1:
            completion = client.chat.completions.create(
                temperature=0,
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": I_prompt + data['answer']}
                ]
            )
            response = completion.choices[0].message.content
            response = re.sub(r'```json|```', '', response)
            response = response.strip()

            try:
                parsed_dict = json.loads(response)
                data['ifI'] = parsed_dict['ifI']
                if parsed_dict['ifI'] == 'yes':
                    data['I'] = parsed_dict['I']
                    data['scoreI'] = parsed_dict['scoreI']
                done = True
                print('valid')
            except json.JSONDecodeError as e:
                print(f"error: {str(e)}, error answer: {response}")
                if 'error' in data:
                    data['error'].append(response)
                else:
                    data['error']=[response]
            
            attempts += 1
            if done:
                break

        # save on the fly
        with open(filename, 'a+', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    proxy_on()
    client = OpenAI( 
        organization="",
        api_key="",
    )
    opts = get_opts()
    run_with_retry(evaluate,opts.datafilename)
    print(f"Finish: {opts.datafilename}")
