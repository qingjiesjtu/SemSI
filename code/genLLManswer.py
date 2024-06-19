from openai import OpenAI
import json
import os
from utils import *
import pandas as pd
from tqdm import tqdm


def query(opts,resume=True):
    proxy_on()
    client = OpenAI( 
        organization="",
        api_key="",
    )

    modelName=opts.model_name
    sourcefile=opts.source_file
    savedir=os.path.join("exp",sourcefile.split('/')[-2])
    os.makedirs(savedir, exist_ok=True)
    savefile=savedir+'/'+modelName+".jsonl"
    question=opts.question
    dataFrame = pd.read_json(sourcefile)
    line_count = 0
    if resume and os.path.exists(savefile):
        with open(savefile, 'r', encoding='utf-8') as file:
            line_count = sum(1 for line in file)

    for index, row in tqdm(dataFrame.iterrows(), total=dataFrame.shape[0]):
        if index<line_count: continue
        data = row.to_dict()
        statement = data['statement'][:-1] if data['statement'][-1]=='.' else data['statement']
        prompt=question+statement+'?'
        if 'instruct' in modelName:
            response = client.completions.create(
                model=modelName,
                prompt=prompt,
                max_tokens=512 

            )
            answer=response.choices[0].text
        else:
            completion = client.chat.completions.create(
                model=modelName,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            answer=completion.choices[0].message.content
        data['prompt']=prompt
        data['model']=modelName
        data['answer']=answer
        with open(savefile, 'a') as file2:
            json_line = json.dumps(data)
            file2.write(json_line + '\n')
    print("All done!")
    proxy_off()

if __name__ == '__main__':
    opts = get_opts()
    run_with_retry(query,opts)
