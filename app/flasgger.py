template = {
    "swagger": "2.0",
    "info": {
        "title": "API - Lista de Tarefas",
        "description": "Esta é a documentação de acesso a api do projeto lista de tarefas",
        "contact": {
            "responsibleOrganization": "QueirozT",
            "responsibleDeveloper": "QueirozT",
            "email": "contato@queirozt.webredirect.org",
            "url": "https://github.com/queirozt",
        },
        "termsOfService": "https://mit-license.org/",
        "version": "1.0.0"
    },
    "host": 'lista-de-tarefas.queirozt.webredirect.org',
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "\
            JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ],
    "definitions": {
        "Register": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "example": "exemplo@email.com"
                },
                "password": {
                    "type": "string",
                    "example": "Nova senha"
                },
                "username": {
                    "type": "string",
                    "example": "Nome do usuário"
                },
            }
        },
        "Auth": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "example": "exemplo@email.com"
                },
                "password": {
                    "type": "string",
                    "example": "Senha do usuário"
                },
            }
        },
        "Tarefas": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/Tarefa"
            }
        },
        "Tarefa": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "example": "Um título"
                },
                "description": {
                    "type": "string",
                    "example": "Uma Descrição"
                },
                "type": {
                    "type": "string",
                    "example": "lista"
                },
                "priority": {
                    "type": "boolean",
                    "example": False
                },
                "id": {
                    "type": "integer",
                    "example": 1
                }
            }
        },
    }
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apispec/"
}


specs_register = {
    "tags": [
        "Auth"
    ],
    "summary": "Rota para criação de usuário",
    "description": "Cria um novo usuário com os dados informados",
    "parameters": [
        {
            "name": "Register",
            "description": "Modelo para criação de usuário",
            "in": "body",
            "required": "true",
            "schema": {
                "$ref": "#/definitions/Register"
            },
        }
    ],
    "responses": {
        "200": {
            "description": "Usuário registrado com sucesso",
            "schema": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "example": "Nome do usuário"
                    },
                    "email": {
                        "type": "string",
                        "example": "E-mail do usuário"
                    }
                }
            }
        },
        "400": {
            "description": "Erro ao registrar novo usuário",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "list",
                        "example": "Error Message"
                    }
                }
            }
        },
    }
}


specs_get_token = {
    "tags": [
        "Auth"
    ],
    "summary": "Rota de autenticação",
    "description": "Gera um novo token para o usuário informado",
    "parameters": [
        {
            "name": "Get-Token",
            "description": "Modelo de autenticação",
            "in": "body",
            "required": "true",
            "schema": {
                "$ref": "#/definitions/Auth"
            },
        }
    ],
    "responses": {
        "200": {
            "description": "Autenticado com sucesso",
            "schema": {
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "example": "<Token>"
                    }
                }
            }
        },
        "400": {
            "description": "Erro de autenticação",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "list",
                        "example": "Usuário ou senha inválidos"
                    }
                }
            }
        },
    }
}


specs_create = {
    "tags": [
        "Tarefas"
    ],
    "summary": "Rota para criação de uma nova tarefa",
    "description": "Cria uma nova tarefa para o usuário autenticado",
    "parameters": [
        {
            "name": "Tarefa",
            "description": "Um modelo para criação da tarefa",
            "in": "body",
            "required": "true",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "example": "Um título"
                    },
                    "description": {
                        "type": "string",
                        "example": "Uma Descrição"
                    },
                    "type": {
                        "type": "string",
                        "example": "lista"
                    },
                    "priority": {
                        "type": "boolean",
                        "example": False
                    }
                }
            },
        }
    ],
    "responses": {
        "201": {
            "description": "Uma nova tarefa criada com sucesso",
            "schema": {
                "$ref": "#/definitions/Tarefa"
            },
        },
        "400": {
            "description": "Erro no modelo",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "list",
                        "example": ["Error Message"]
                    }
                }
            }
        },
        "401": {
            "description": "Token Inválido",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Invalid Token"
                    }
                }
            }
        },
        "403": {
            "description": "Acesso negado",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Access Denied"
                    }
                }
            }
        }
    }
}

specs_collect = {
    "tags": [
        "Tarefas"
    ],
    "summary": "Rota para coletar as tarefas",
    "description": "Coleta todas as tarefas do usuário autenticado",
    "responses": {
        "200": {
            "description": "Lista com todas as tarefas do usuário",
            "schema": {
                "$ref": "#/definitions/Tarefas"
            },
        },
        "401": {
            "description": "Token Inválido",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Invalid Token"
                    }
                }
            }
        },
        "403": {
            "description": "Acesso negado",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Access Denied"
                    }
                }
            }
        }
    }
}

specs_update = {
    "tags": [
        "Tarefas"
    ],
    "summary": "Rota para atualizar uma tarefa existente",
    "description": "Atualiza os dados de uma tarefa existente",
    "parameters": [
        {
            "name": "id",
            "description": "ID da tarefa a ser atualizada",
            "in": "path",
            "required": "true",
            "type": "integer",
            "example": 1
        },
        {
            "name": "Tarefa",
            "description": "Um modelo para edição da tarefa",
            "in": "body",
            "required": "true",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "example": "Um título"
                    },
                    "description": {
                        "type": "string",
                        "example": "Uma Descrição"
                    },
                    "type": {
                        "type": "string",
                        "example": "lista"
                    },
                    "priority": {
                        "type": "boolean",
                        "example": False
                    }
                }
            },
        }
    ],
    "responses": {
        "201": {
            "description": "Tarefa atualizada com sucesso",
            "schema": {
                "$ref": "#/definitions/Tarefa"
            },
        },
        "400": {
            "description": "Erro no modelo",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "list",
                        "example": "Error Message"
                    }
                }
            }
        },
        "401": {
            "description": "Token Inválido",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Invalid Token"
                    }
                }
            }
        },
        "403": {
            "description": "Acesso negado",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Access Denied"
                    }
                }
            }
        }
    }
}

specs_delete = {
    "tags": [
        "Tarefas"
    ],
    "summary": "Rota para deletar uma tarefa existente",
    "description": "Remove uma tarefa existente do banco de dados",
    "parameters": [
        {
            "name": "id",
            "description": "ID da tarefa a ser deletada",
            "in": "path",
            "required": "true",
            "type": "integer",
            "example": 1
        }
    ],
    "responses": {
        "204": {
            "description": "Tarefa deletada com sucesso",
        },
        "400": {
            "description": "Tarefa não encontrada",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "list",
                        "example": {1: "Not Found"}
                    }
                }
            }
        },
        "401": {
            "description": "Token Inválido",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Invalid Token"
                    }
                }
            }
        },
        "403": {
            "description": "Acesso negado",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Access Denied"
                    }
                }
            }
        }
    }
}