# engine/ — cópia fiel do motor do ESP32

Estes arquivos são **cópias byte a byte** de
[`pganaclara/esp32_crypto`](https://github.com/pganaclara/esp32_crypto),
pasta `des_distributed/`, no commit:

```
bf0efe60003200111fb71f822b9f1605fc8f9feb   (2026-09-25)
"Docs: FMS single-board numbers from the run on core 3.3.12"
```

| arquivo | papel |
|---|---|
| `des_generic.h` | o motor: criptografia EC-ElGamal, protocolo (2PC / NOTIFY), roteamento, oráculo |
| `des_transport.h` | transporte UDP/IP multicast (RFC 1112) |
| `supervisor_data_fms.h` | os 7 supervisores do FMS, gerados pelo notebook UltraDES (os outros problemas do `esp32_crypto` não são usados aqui) |

**Nada aqui é editado.** Tudo o que é específico de container fica em `../src/`
(ponto de entrada, chave em tempo de execução, emulação do custo de decifração). É isso que
permite afirmar que o container executa *o mesmo código* que as placas ESP32:
qualquer diferença de comportamento vem da plataforma, não de uma reescrita.

`SHA256SUMS` guarda os hashes. Para conferir:

```bash
cd engine && sha256sum -c SHA256SUMS
```

Para atualizar a partir de um commit mais novo do `esp32_crypto`, use
`scripts/sync-engine.sh <caminho-do-clone>`: ele copia os arquivos, recalcula os
hashes e registra o commit aqui.
