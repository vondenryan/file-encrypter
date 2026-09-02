from pathlib import Path
from cryptography.fernet import Fernet


def obter_nome_disponivel(caminho):
    """Evita sobrescrever arquivos existentes."""

    if not caminho.exists():
        return caminho

    contador = 1
    stem = caminho.stem
    suffix = caminho.suffix

    while True:
        novo_caminho = caminho.with_name(
            f"{stem}.{contador}{suffix}"
        )

        if not novo_caminho.exists():
            return novo_caminho

        contador += 1


def criptografar_arquivo():
    print("\n" + "=" * 50)
    print("🔐 CRIPTOGRAFAR ARQUIVO")
    print("=" * 50)

    caminho = input(
        "\n📁 Digite ou cole o caminho do arquivo: "
    ).strip().strip('"')

    arquivo = Path(caminho)

    if not arquivo.exists() or not arquivo.is_file():
        print("\n❌ Arquivo inválido ou não encontrado.")
        return

    try:
        # Gera uma chave única
        chave = Fernet.generate_key()
        fernet = Fernet(chave)

        # Lê o arquivo
        dados = arquivo.read_bytes()

        # Criptografa
        dados_criptografados = fernet.encrypt(dados)

        # Define o arquivo de saída
        arquivo_saida = arquivo.with_name(
            arquivo.name + ".encrypted"
        )

        arquivo_saida = obter_nome_disponivel(
            arquivo_saida
        )

        # Salva o arquivo criptografado
        arquivo_saida.write_bytes(
            dados_criptografados
        )

        print("\n" + "=" * 50)
        print("✅ ARQUIVO CRIPTOGRAFADO COM SUCESSO!")
        print("=" * 50)

        print(f"\n📁 Arquivo original:")
        print(arquivo)

        print(f"\n🔒 Arquivo criptografado:")
        print(arquivo_saida)

        print("\n🔑 CHAVE DE DESCRIPTOGRAFIA:")
        print("-" * 50)
        print(chave.decode())
        print("-" * 50)

        print(
            "\n⚠️ IMPORTANTE: guarde esta chave!"
        )

        print(
            "Sem a chave correta, o arquivo não poderá "
            "ser recuperado."
        )

        print(
            "\n✅ O arquivo original não foi apagado."
        )

    except Exception as erro:
        print(
            f"\n❌ Erro ao criptografar: {erro}"
        )


def descriptografar_arquivo():
    print("\n" + "=" * 50)
    print("🔓 DESCRIPTOGRAFAR ARQUIVO")
    print("=" * 50)

    caminho = input(
        "\n📁 Digite o caminho do arquivo criptografado: "
    ).strip().strip('"')

    arquivo = Path(caminho)

    if not arquivo.exists() or not arquivo.is_file():
        print("\n❌ Arquivo inválido ou não encontrado.")
        return

    chave = input(
        "\n🔑 Cole a chave de descriptografia: "
    ).strip()

    if not chave:
        print("\n❌ Nenhuma chave informada.")
        return

    try:
        # Cria o objeto de descriptografia
        fernet = Fernet(chave.encode())

        # Lê o arquivo criptografado
        dados_criptografados = arquivo.read_bytes()

        # Descriptografa
        dados_originais = fernet.decrypt(
            dados_criptografados
        )

        # Remove .encrypted do nome
        if arquivo.name.endswith(".encrypted"):
            nome_original = arquivo.name[
                :-len(".encrypted")
            ]
        else:
            nome_original = (
                arquivo.stem + ".decrypted"
            )

        arquivo_saida = arquivo.with_name(
            nome_original
        )

        arquivo_saida = obter_nome_disponivel(
            arquivo_saida
        )

        # Salva o arquivo recuperado
        arquivo_saida.write_bytes(
            dados_originais
        )

        print("\n" + "=" * 50)
        print("✅ ARQUIVO DESCRIPTOGRAFADO COM SUCESSO!")
        print("=" * 50)

        print(f"\n📁 Arquivo recuperado:")
        print(arquivo_saida)

        print(
            "\n✅ O arquivo criptografado não foi apagado."
        )

    except Exception:
        print(
            "\n❌ Não foi possível descriptografar."
        )

        print(
            "Verifique se a chave está correta e se "
            "o arquivo não foi alterado."
        )


def main():
    while True:
        print("\n" + "=" * 50)
        print("🔐 GERENCIADOR DE CRIPTOGRAFIA")
        print("=" * 50)

        print("\n[1] 🔒 Criptografar arquivo")
        print("[2] 🔓 Descriptografar arquivo")
        print("[3] ❌ Sair")

        escolha = input(
            "\nEscolha uma opção: "
        ).strip()

        if escolha == "1":
            criptografar_arquivo()

        elif escolha == "2":
            descriptografar_arquivo()

        elif escolha == "3":
            print("\n👋 Programa encerrado.")
            break

        else:
            print(
                "\n❌ Opção inválida."
            )

        input(
            "\nPressione ENTER para voltar ao menu..."
        )


if __name__ == "__main__":
    main()