import yaml

if __name__ == '__main__':
    with open('sample.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        for key in data:
            print(key)
