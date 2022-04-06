import argparse
import yaml
from cfn_tools import load_yaml, dump_yaml
import cfn_flip.yaml_dumper



def edit_yaml(type,stack_name):
    with open(f'packaged-{type}.yaml') as f:
        raw = f.read()
    yaml_dict = load_yaml(raw)

    for i in yaml_dict["Resources"]:
        if yaml_dict["Resources"][i]["Type"] == "AWS::Serverless::Function": #Search for lambda function and edit the function name
            yaml_dict["Resources"][i]["Properties"]["FunctionName"] = f"{stack_name}-{i}"  
        
        elif yaml_dict["Resources"][i]["Type"] == "AWS::SQS::Queue": #Search for queue and edit the queue name
            yaml_dict["Resources"][i]["Properties"]["QueueName"] = f"{stack_name}-{i}"  

        elif yaml_dict["Resources"][i]["Type"] == "AWS::S3::Bucket": #Search for s3 and edit the s3 bucket name
            yaml_dict["Resources"][i]["Properties"]["BucketName"] = f"{stack_name}-{i}"  
    
   
    #rewrite the yaml file
    with open(f'packaged-{type}.yaml','w+') as f:
        dumper = cfn_flip.yaml_dumper.get_dumper(clean_up=False, long_form=False)
        raw = yaml.dump(
            yaml_dict,
            Dumper=dumper,
            default_flow_style=False,
            allow_unicode=True
        )

        f.write(raw)

def main():
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-i", "--input", help = "Input Option") #Choose test or prod
    parser.add_argument("-s","--stack_name", help="Input Stack Name")

    # Read arguments from command line
    args = parser.parse_args()

    stack_name = args.stack_name

    if args.input:
        if args.input == 'testing':
            #do test stuff
            print("Updating Test Stack Yaml")
            edit_yaml('testing', stack_name)
        elif args.input == 'prod':
            #do the prod stuff
            print("Updating Prod Stack Yaml")
            edit_yaml('prod', stack_name)
        else: 
            print("No stack")

if __name__ == "__main__":
    # calling the main function a
    main()
