from socket import *
import ssl
import base64

# Some global variables
SMTP_MAIL_SERVER = 'smtp-mail.outlook.com'
SMTP_TLS_PORT = 587
END_MESSAGE = '\r\n.\r\n'

client_socket = None
ssl_context = None


def send_line(line):
    global client_socket
    print('CLIENT: ' + line.strip())
    client_socket.send(line.encode())
    response = client_socket.recv(1024).decode()
    return response


def get_code(response):
    return int(response[:3])


def connect():
    global client_socket
    global ssl_context
    print('CLIENT: Connecting to ' + SMTP_MAIL_SERVER)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((SMTP_MAIL_SERVER, SMTP_TLS_PORT))
    response = client_socket.recv(1024).decode()
    return response


def send_ehlo():
    helo = 'ehlo smtp-mail.outlook.com\r\n'
    return send_line(helo)


def send_helo():
    helo = 'helo smtp-mail.outlook.com\r\n'
    return send_line(helo)


def start_tls():
    global client_socket
    global ssl_context
    response = send_line('STARTTLS \r\n')
    ssl_context = ssl._create_stdlib_context()
    client_socket = ssl_context.wrap_socket(client_socket, server_hostname=SMTP_MAIL_SERVER)
    return response


def send_auth_request():
    return send_line('auth login \r\n')


def send_username(username):
    as_bytes = username.encode('ascii')
    as_b64 = base64.b64encode(as_bytes)
    as_utf8 = as_b64.decode('utf-8')
    return send_line(as_utf8 + '\r\n')


def send_password(password):
    as_bytes = password.encode('ascii')
    as_b64 = base64.b64encode(as_bytes)
    as_utf8 = as_b64.decode('utf-8')
    return send_line(as_utf8 + '\r\n')


'''--------------------------------------------------------------------------------
TODO - Implement the functions below this point in order to send a test
       email successfully using SMTP commands  
--------------------------------------------------------------------------------'''

def send_mail_from(sender):
    mail_from = f'MAIL FROM: <{sender}>\r\n'
    return send_line(mail_from)


def send_rcpt_to(recipient):
    mail_to = f'RCPT TO: <{recipient}>\r\n'
    return send_line(mail_to)



def send_begin_data():
    return send_line('DATA\r\n')


def send_message(subject, message):
    data_to_be_sent = f'Subject: {subject} \r\n\r\n {message} \r\n\r\n {END_MESSAGE}'
    return send_line(data_to_be_sent)


def send_quit():
    return send_line('QUIT \r\n')

def get_user_input(user_msg: str) ->str:
    try:
        while True: # Please note: Infinite loop
            value = input(user_msg)
            if len(value.strip()) < 1:
                print("Please enter a value")
                continue
            return str(value)
    except Exception as e:
        print(f"Error: {e}")
        return False



'''--------------------------------------------------------------------------------
TODO - Implement the functions above this point in order to send a test
       email successfully using SMTP commands  
--------------------------------------------------------------------------------'''

import traceback

def send_one_email():
    # Open a TCP connection - the reply should start '220'
    reply = connect()
    print('SERVER: ' + reply)
    # Send a EHLO command - the reply should be a list of supported
    # 'enhanced' SMTP functions each starting '250'
    reply = send_ehlo()
    print('SERVER: ' + reply)
    # Ask the server to switch to TLS - reply should start '220'
    reply = start_tls()
    print('SERVER: ' + reply)
    # Send a HELO command encrypted - reply should start '220'
    reply = send_helo()
    print('SERVER: ' + reply)
    # Send an AUTH LOGIN command
    reply = send_auth_request()
    print('SERVER: ' + reply)
    # Send your (base64 encoded username) -
    reply = send_username('top123ii5@outlook.com')
    print('SERVER: ' + reply)
    # Send your (base64 encoded username) -
    reply = send_password('Magagee@2M')
    print('SERVER: ' + reply)
    # Send MAILFROM command - TODO - YOU IMPLEMENT THE FUNCTION BELOW
    reply = send_mail_from('top123ii5@outlook.com')
    print('SERVER: ' + reply)
    # Send RCPT TO command - TODO - YOU IMPLEMENT THE FUNCTION BELOW
    reply=send_rcpt_to('top123ii5@outlook.com')
    print('SERVER: ' + reply)
    # Send DATA command - TODO - YOU IMPLEMENT THE FUNCTION BELOW
    reply = send_begin_data()
    print('SERVER: ' + reply)
    # Send the message (including subject) - TODO - YOU IMPLEMENT THE FUNCTION BELOW
    # GETS THE USER INPUT
    subject = get_user_input("What is the Subject of the email? ")
    body = get_user_input("What is the Body message of the email? ")
    reply = send_message(subject=subject, message=body)
    print('SERVER: ' + reply)
    # Quit the SMTP session - TODO - YOU IMPLEMENT THE FUNCTION BELOW
    reply = send_quit()
    
    print('SERVER: ' + reply)




if __name__ == '__main__':
    send_one_email()
