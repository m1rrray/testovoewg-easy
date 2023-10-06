import argparse

import requests




def create_session(password):
    headers = {
        "Content-Type": "application/json",
        "Cookie": "connect.sid=s%3AzEyHv8u1mxxizVoXwVZmK3HAysZAWTaR.B9UqU4KNXGDQWp1zXP755WQnLLH%2FuWG4Hu9NDUmRWBA"
    }
    body = {"password": password}
    response = requests.post(url + "session", headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()  # Предполагается, что сервер возвращает JSON-данные
        print(data)
    else:
        print(f"Ошибка: {response.status_code}")


def get_session():
    headers = {
        "Content-Type": "application/json",
        "Cookie": "connect.sid=s%3AzEyHv8u1mxxizVoXwVZmK3HAysZAWTaR.B9UqU4KNXGDQWp1zXP755WQnLLH%2FuWG4Hu9NDUmRWBA"
    }
    response = requests.get(url + "session", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Ошибка: {response.status_code}")


def get_clients():
    headers = {
        "Content-Type": "application/json",
        "Cookie": "connect.sid=s%3AzEyHv8u1mxxizVoXwVZmK3HAysZAWTaR.B9UqU4KNXGDQWp1zXP755WQnLLH%2FuWG4Hu9NDUmRWBA"
    }
    response = requests.get(url + "wireguard/client", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
        # print(data)
    else:
        print(f"Ошибка: {response.status_code}")


def create_client(name):
    headers = {
        "Content-Type": "application/json",
        "Cookie": "connect.sid=s%3AzEyHv8u1mxxizVoXwVZmK3HAysZAWTaR.B9UqU4KNXGDQWp1zXP755WQnLLH%2FuWG4Hu9NDUmRWBA"
    }
    data = {
        "name": name
    }
    response = requests.post(url + "wireguard/client", json=data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Ошибка: {response.status_code}")


def get_configuration(client_id):
    headers = {
        "Content-Type": "application/json",
        "Cookie": "connect.sid=s%3AzEyHv8u1mxxizVoXwVZmK3HAysZAWTaR.B9UqU4KNXGDQWp1zXP755WQnLLH%2FuWG4Hu9NDUmRWBA"
    }
    urln = url + f'wireguard/client/{client_id}/configuration'
    response = requests.get(urln, headers=headers)
    if response.status_code == 200:
        with open('./first.conf', 'wb') as f:
            f.write(response.content)
    else:
        print(f"Ошибка: {response.status_code}")


def create_client_get_conf(name):
    headers = {
        "Content-Type": "application/json",
        "Cookie": "connect.sid=s%3AzEyHv8u1mxxizVoXwVZmK3HAysZAWTaR.B9UqU4KNXGDQWp1zXP755WQnLLH%2FuWG4Hu9NDUmRWBA"
    }
    data = {
        "name": name
    }
    response = requests.post(url + "wireguard/client", json=data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        name = data['name']
        address = data['address']
        clients = get_clients()
        for client in clients:
            if client['address'] == address:
                client_id = client['id']
                break
        urln = url + f'wireguard/client/{client_id}/configuration'
        file = requests.get(urln, headers=headers)
        if file.status_code == 200:
            with open('./sec.conf', 'wb') as f:
                f.write(file.content)
        else:
            print(f"Ошибка: {file.status_code}")
    else:
        print(f"Ошибка: {response.status_code}")


def parse_args():
    parser = argparse.ArgumentParser(description="Описание вашей программы")
    parser.add_argument("command",
                        choices=["create_session", "get_session", "get_clients", "create_client", "get_configuration",
                                 "create_client_get_conf"],
                        help="Выберите одну из доступных команд")
    parser.add_argument("--name", help="Аргумент для create_client")
    parser.add_argument("--client_id", help="Аргумент для get_configuration")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if args.command == "create_session":
        create_session(args.password)
    elif args.command == "get_session":
        get_session()
    elif args.command == "get_clients":
        print(get_clients())
    elif args.command == "create_client":
        create_client(args.name)
    elif args.command == "get_configuration":
        get_configuration(args.client_id)
    elif args.command == "create_client_get_conf":
        create_client_get_conf(args.name)


if __name__ == "__main__":
    main()


# get_session()
# get_clients()
# create_client('misha3')

