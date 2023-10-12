# Atividades Práticas Supervisionadas

## Proposta

O grupo de alunos deve desenvolver, em Python, Java ou C#, uma ferramenta de identificação e autenticação biométrica que restrinja o acesso a uma rede com banco dados do Ministério do Meio Ambiente. 

As informações são estratégicas sobre as propriedades rurais que utilizam agrotóxicos proibidos por causarem grandes impactos nos lenções freáticos, rios e mares. 

As informações de nível 1 todos podem ter acesso; as de nível 2 são restritas aos diretores de divisões; as de nível 3 somente são acessadas pelo ministro do
meio ambiente.

## Configuração do Ambiente
- Instalar  e ativar o Ambiente virtual do Pyhton

    ```python
    conda create --name apsvm python=3.9 
    conda activate apsvm 
    ```
- Instalar Dependências e Bibliotecas necessárias para o funcionamento da aplicação

        ```python
        pip install opencv-python 
        pip install numpy
        pip install cmake
        pip install boost
        conda install -c conda-forge c
        pip install face_recognition
        ```

## Autores

- Beatriz Chieffi
- Mateus Pavesi
- Rafael Souza
