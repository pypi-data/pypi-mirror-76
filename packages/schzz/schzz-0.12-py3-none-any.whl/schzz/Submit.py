import requests

def make_post(username, password, model_json , acc, val_acc, loss, val_loss, title, evaluate, report):
  data = {'username':username,
            'password':password}
  x = requests.post(('http://schwarzam.art/api/auth/login'), data=data, json={'Content-Type': 'application/json'})

  if x.status_code == 200:
    x = (x.json())
    token = x['token']
    username = x['user']['username']
    email = x['user']['email']

    jsnono = {'Content-Type': 'application/json'}
    headers = {'Authorization' : f'token {token}'}

    acc = str(list(acc))
    val_acc = str(list(val_acc))
    loss = str(list(loss))
    val_loss = str(list(val_loss))
    evaluate =f'{evaluate}'

    data = {'name': f'{username}',
            'email': f'{email}',
            'title': f'{title}',
            'model_json': model_json,
            'evaluate': evaluate,
            'report': report,
            'acc': (f'{(acc)}'),
            'val_acc': (f'{(val_acc)}'),
            'loss': (f'{(loss)}'),
            'val_loss': (f'{(val_loss)}')}

    response = requests.post('http://schwarzam.art/api/leadsML/', data=data, json=jsnono, headers=headers)
    print(response.status_code ,'done')
  else:
      print('Failed!')
