# whatsapp-chatbot-template

This is the template app for using integration with whatsapp business API.

## Requirements

- installed python3.10 or newer
- installed docker

## 1. Setup

- Create and fill dotenv file (`./whatsapp-webhook-template/.env`) from [example file](./whatsapp-webhook-template/backend/config/environment/env.sh.template)
- You can simple run sample app by typing `make launch`

## 2. Writing bot answer realisation

You can implement your own answer logic [here](./whatsapp-webhook-template/backend/tasks/message_processing/whatsapp_processing_service.py) (row 289)  
By default bot works as echo service.
