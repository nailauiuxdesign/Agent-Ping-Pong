# Helloworld Agent

Este agente responde "goodbye world" si recibe la cadena "helloworld" por stdin (protocolo MCP).

## Ejemplo de mensaje de entrada
```json
{"sender": "test", "content": "helloworld"}
```

## Ejemplo de respuesta
```json
{"sender": "helloworld-agent", "receiver": "test", "content": "goodbye world"}
```

## Uso
Puedes lanzar el agente con:
```bash
./run_agent.sh
```

---

## Integración en Coral Server
Agrega la siguiente sección al bloque `registry` de `coral/application.yaml`:

```yaml
  helloworld:
    options: []
    runtime:
      type: "executable"
      command: ["bash", "-c", "../agents/helloworld/run_agent.sh ../agents/helloworld/main.py"]
```

Esto permitirá que Coral Server lance el agente y le envíe mensajes por stdin. El agente permanecerá esperando nuevas peticiones.
