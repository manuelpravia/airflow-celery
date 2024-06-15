FROM ubuntu:latest

# Instalar SSH
RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd

# Copiar el script de Python al contenedor
#COPY generar_data.py /root/generar_data.py

# Configurar el servidor SSH
RUN echo 'root:password' | chpasswd 
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords yes/' /etc/ssh/sshd_config

EXPOSE 22

# Ejecutar el servidor SSH
CMD ["/usr/sbin/sshd", "-D"]


#Comado para geerar la imagen
# docker build -t server_ssh_imag .
