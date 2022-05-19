import boto3 

REGION = 'us-east-1'

def get_all_alb_arn() -> tuple:
    alb = boto3.client('elbv2', region_name=REGION)
    return  ([lb.get('LoadBalancerArn') for lb in alb.describe_load_balancers().get('LoadBalancers')], alb)

def get_all_alb_listeners(alb_arns: list, botoClient: boto3) -> tuple:
    alb_listeners = [botoClient.describe_listeners(LoadBalancerArn=lb)['Listeners'] for lb in alb_arns]
    
    container = []
    for i, _ in enumerate(alb_listeners):
        try:
            #anonymous (lambda) function invoked once each pass - each iter passes index of list(which is also a list)
            container.append({(lambda x: x[0]['ListenerArn'])(alb_listeners[i]): \
                (lambda x: x[0]['LoadBalancerArn'])(alb_listeners[i])})
        except Exception as e:
            print(e)
    
    # print(container)
    return container, botoClient

def extract_target_group_type(listener_alb_map:list,botoClient: boto3) -> None:
    
    #dictionary comprehension 
    r = { botoClient.describe_target_groups(LoadBalancerArn=str(list(i.values())[0]))\

        ['TargetGroups'][0]['TargetType']: \

         str(list(i.keys())[0]) for i in listener_alb_map
         }

    print(r)
    return r
    
def init():
    res, client = get_all_alb_arn()
    kwargs = {"alb_arns":res, "botoClient": client}
    listener_arns, client = get_all_alb_listeners(**kwargs)
    extract_target_group_type(listener_arns, client)


if __name__ == "__main__":

    init()


#Elliott Arnold - small utility that will provide a mapping of alb_arn or listener_arn and yarget group type
#5-18-22 7-11  OTJ BYOT tools  list, dictionary comprehension and lambda practice
