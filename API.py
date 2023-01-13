import json 
import netmiko
from netmiko import ConnectHandler
#se importan las librerias necesias

mac=input("ingresa tu mac :  ")#se le pide al usuario que imgrese la mac
Usuario=input("ingresa el usuario: " )#se necesita que se ingrese el usuario 
Contraseña=input("ingresa la contraseña: ")
Ip=input("ingresa la ip: ")


cisco= {
    "device_type": "cisco_ios",#intenta entrar a el SW con las credenciales ingresadas
    "host": Ip,
    "username": Usuario,
    "password": Contraseña
}

net_connect = ConnectHandler(**cisco) #intentamos conectar al SW con las credenciales 
net_connect.enable()
#CONEXION------------------------------------------------------------------------------------------

while True:
    #BUSQUEDA CDP---------------------
    output = net_connect.send_command('show cdp neighbors detail', use_textfsm= True )#agregamos el comando"shw cdp neighbors" para buscar vecionos (use_textfsm= True )no sirve para traducir a formato json, y asi las busqueda sea mas facil
    output=(json.dumps(output, indent= 2))
    output=json.loads(output)
    #print(output)

    #BUSQUEDA MAC---------------------
    output1= net_connect.send_command('sh mac address-table', use_textfsm= True )#el comando sirve para mostrar la tabla 
    output1=(json.dumps(output1, indent= 2))#usamos esta linea de codigo para tener la tabla de mac addres en jason
    output1=json.loads(output1)
    #print(output1)#se imprime la tabla 

    #POR CADA HOST EN LA LISTA DE MACS COMPARA SU MAC, CON LA MAC QUE SE BUSCA
    for host in range (len(output1)):
        macm=output1[host]['destination_address']
        if macm == mac:#SI LA MAC QUE BUSCAMOS, ESTA EN LA LISTA DE HOSTS
            puertom=output1[host]["destinantion_port"]#OBTENEMOS EL PUERTO EN EL QUE ESTA LA MAC

        else:#SI NO ENCUENTRA LA MAC DENTRO DE LA LISTA, ESA MAC, NO EXISTE EN LA TABLA
            puertom=" "

    for vecino in range (len(output)):  #esta parte se utiliza para ir preguntado a cada vecino todosd los parametros que estan dentro del for
    
        interfaz_vecino= output[vecino][ "local_port"]#SACA EL PUERTO DE CADA VECINO
    if puertom == interfaz_vecino:#COMPARA EL PUERTO DEL VECINO, CON EL PUERTO POR EL QUE ENCONTRO LA MAC (PUERTOM)
        ip_vecino=output[vecino]['management_ip']#SI EL PUERTO COINCIDE, SE OBTIENE LA IP DEL VECINO
    else:#SI EL PUERTO NO COINCIDE, SIGNIFICA, QUE ESE PUERTO, ES LA MAC QUE BUSCAMOS
        print('''
        AQUI DEBE IMPRIMIR EL NOMBRE DEL SWITCH EN EL QUE SE ENCUENTRA LA MAC
        LA IP DEL VECINO Y EL PUERTO EN EL QUE ENCONTRO LA MAC EJ:
        LA MAC X(MAC COMPLETA) SE ENCONTRO EN EL PUERTO FAX/X/X(EL PUERTO) DEL (NOMBRE DEL SWITCH) 
        ''')

    try:#SI LOGRA OBTENER CORRECTAMENTE, LA IP DEL VECINO, Y SE INTENTA CONECTAR, USANDO EL USUARIO Y CONTRASEÑA QUE SE DIO AL PRINCIPIO
        cisco= {
            "device_type": "cisco_ios",#intenta entrar a el SW1 con las credenciales ingresadas
            "host": ip_vecino,
            "username": Usuario,
            "password": Contraseña
        }

        net_connect = ConnectHandler(**cisco) #intentamos conectar al SW1 con las credenciales 
        net_connect.enable()
    except:
        print("Se encntro la mac")
        
        break






