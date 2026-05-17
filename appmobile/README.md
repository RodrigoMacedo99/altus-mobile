# Altus Mobile App

Este é um aplicativo Android desenvolvido para monitoramento e controle de kits de automação (Kit 1 e Kit 2) através do protocolo MQTT.

## 🚀 Funcionalidades

- **Controle em Tempo Real**: Envio de comandos para botões pulsadores e interruptores via MQTT.
- **Monitoramento de Status**: Visualização do estado atual de saídas digitais (LEDs) recebendo atualizações via broker MQTT.
- **Suporte a Múltiplos Kits**: Interface dedicada para o Kit 1 e Kit 2 da Altus.
- **Visualizador de Logs**: Tela integrada para acompanhar as mensagens enviadas e recebidas pelo aplicativo (usada principalmente no desenvolvimento e debug).
- **Configuração Flexível**: Suporte a diferentes brokers MQTT, portas, autenticação e SSL.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: [Kotlin](https://kotlinlang.org/)
- **SDK**: Android SDK (Target SDK 36, Min SDK 24)
- **Arquitetura**: MVVM (Model-View-ViewModel)
- **Comunicação**: [HiveMQ MQTT Client](https://github.com/hivemq/hivemq-mqtt-client) para Android.
- **Interface**: XML Layouts com ConstraintLayout e Material Components.

## ⚙️ Configuração do Projeto

O projeto utiliza o arquivo `local.properties` para gerenciar as credenciais do broker MQTT de forma segura, sem expô-las no controle de versão.

1.  Localize o arquivo `local.properties.example` na raiz do projeto `AltusMobileApp`.
2.  Crie uma cópia deste arquivo e renomeie para `local.properties`.
3.  Preencha as variáveis com os dados do seu broker (caso não tenha senha e usuário, apenas deixe em branco):

```properties
mqtt.url=seu-broker.com
mqtt.user=seu-usuario
mqtt.password=sua-senha
mqtt.port=sua-porta
mqtt.use_ssl=true
```

O `build.gradle.kts` do módulo `app` está configurado para ler estas propriedades e injetá-las no `BuildConfig` da aplicação.

## 📁 Estrutura do Projeto

- `app/src/main/java/com/example/altusmobileapp/ui`: Contém as Activities e ViewModels da interface do usuário.
- `app/src/main/java/com/example/altusmobileapp/mqtt`: Contém a lógica de conexão e tratamento de mensagens MQTT (`MqttHandler`).
- `app/src/main/res/layout`: Arquivos de definição de layout da interface.

## 📝 Como Executar

1.  Clone este repositório.
2.  Abra o projeto no Android Studio (Giraffe ou superior recomendado).
3.  Configure o arquivo `local.properties` conforme descrito acima.
4.  Sincronize o Gradle.
5.  Execute o aplicativo em um emulador ou dispositivo físico com Android 7.0 (API 24) ou superior.
