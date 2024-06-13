from modelos.Livro import Livro
from estruturas.BinaryTree import BinaryTree
from estruturas.ListaDuplamenteLigada import ListaDuplamenteLigada
from estruturas.Pilha import Pilha
from utils.LimparTela import limpar_tela

class BibliotecaConsole:
    def __init__(self):
        self.arvore = BinaryTree()
        self.lista = ListaDuplamenteLigada()
        self.historico_undo = Pilha()

    def validar_entrada(self, prompt, tipo):
        while True:
            entrada = input(prompt)
            try:
                if tipo == 'int':
                    return int(entrada)
                elif tipo == 'str':
                    return entrada.strip()
            except ValueError:
                print(f"Entrada inválida. Por favor, insira um {tipo} válido.")

    def adicionar_livro(self):
        limpar_tela()
        titulo = self.validar_entrada("\033[1;33mTítulo: \033[0m", 'str')
        autor = self.validar_entrada("\033[1;33mAutor: \033[0m", 'str')
        ano = self.validar_entrada("\033[1;33mAno: \033[0m", 'int')
        genero = self.validar_entrada("\033[1;33mGênero: \033[0m", 'str')
        livro = Livro(titulo, autor, ano, genero)
        if self.arvore.search(titulo):
            print(f"\033[1;31mLivro com título '{titulo}' já existe.\033[0m")
            return
        
        self.arvore.insert(titulo)
        self.lista.append(livro)
        self.historico_undo.push(('add', livro))
        print(f"\033[1;32mLivro '{titulo}' adicionado com sucesso!\033[0m")

    def remover_livro(self):
        limpar_tela()
        titulo = self.validar_entrada("\033[1;33mTítulo do livro a ser removido: \033[0m", 'str').lower()
        atual = self.lista.head
        while atual:
            if atual.value.titulo.lower() == titulo:
                livro_removido = atual.value
                self.lista.remove(atual.value)
                self.arvore.remove(titulo)
                self.historico_undo.push(('remove', atual.value))
                print(f"\033[1;32mLivro '{livro_removido.titulo}' removido com sucesso.\033[0m")
                return  
            atual = atual.next
        print(f"\033[1;31mLivro '{titulo}' não encontrado.\033[0m")

    def buscar_livro(self):
        limpar_tela()
        titulo = self.validar_entrada("\033[1;33mTítulo do livro a ser buscado: \033[0m", 'str')
        atual = self.lista.head
        while atual:
            if atual.value.titulo == titulo:
                livro_encontrado = atual.value
                borda_superior = "\033[1;34m+" + "-"*38 + "+\033[0m"
                borda_inferior = "\033[1;34m+" + "-"*38 + "+\033[0m"
                print(borda_superior)
                print("\033[1;32m|         Livro encontrado             |\033[0m")
                print(borda_inferior)
                print(f"\033[1;34m| Título:  \033[0m{livro_encontrado.titulo:<27} \033[1;34m|\033[0m")
                print(f"\033[1;36m| Autor:   \033[0m{livro_encontrado.autor:<27} \033[1;36m|\033[0m")
                print(f"\033[1;33m| Ano:     \033[0m{livro_encontrado.ano:<27} \033[1;33m|\033[0m")
                print(f"\033[1;35m| Gênero:  \033[0m{livro_encontrado.genero:<27} \033[1;35m|\033[0m")
                print(borda_inferior)
                return
            atual = atual.next
        print(f"\033[1;31mLivro '{titulo}' não encontrado.\033[0m")

    def ordenar_livros(self):
        limpar_tela()
        print("\033[1;34m+" + "-"*38 + "+\033[0m")
        print("\033[1;34m|          Livros ordenados            |\033[0m")
        print("\033[1;34m+" + "-"*38 + "+\033[0m")
        self.arvore.inorder(self._print_livro)

    def _print_livro(self, titulo):
        atual = self.lista.head
        while atual:
            if atual.value.titulo == titulo:
                livro = atual.value
                print(f"\033[1;34m| Título:  \033[0m{livro.titulo:<27} \033[1;34m|\033[0m")
                print(f"\033[1;36m| Autor:   \033[0m{livro.autor:<27} \033[1;36m|\033[0m")
                print(f"\033[1;33m| Ano:     \033[0m{livro.ano:<27} \033[1;33m|\033[0m")
                print(f"\033[1;35m| Gênero:  \033[0m{livro.genero:<27} \033[1;35m|\033[0m")
                print("\033[1;34m+" + "-"*38 + "+\033[0m")
                break
            atual = atual.next

    def desfazer_acao(self):
        limpar_tela()
        if self.historico_undo.is_empty():
            print("\033[1;31mNada para desfazer.\033[0m")
            return
        acao, livro = self.historico_undo.pop()
        if acao == 'add':
            if self.lista.remove(livro):
                self.arvore.remove(livro.titulo)
                print(f"\033[1;32mAção desfeita:\033[0m Adição do livro '{livro.titulo}'")
            else:
                print(f"\033[1;31mErro ao desfazer:\033[0m O livro '{livro.titulo}' não foi encontrado na lista.")
        elif acao == 'remove':
            self.lista.append(livro)
            self.arvore.insert(livro.titulo)
            print(f"\033[1;32mAção desfeita:\033[0m Remoção do livro '{livro.titulo}'")

    def exibir_menu(self):
        while True:
            limpar_tela()
            borda_superior = "\033[1;34m+" + "-"*38 + "+\033[0m"
            borda_inferior = "\033[1;34m+" + "-"*38 + "+\033[0m"
            print(borda_superior)
            print("\033[1;34m|    Biblioteca de Livros Inteligente  |\033[0m")
            print(borda_inferior)
            print("\033[1;32m| 1.\033[0m \033[1;37mAdicionar Livro                   \033[1;32m|\033[0m")
            print("\033[1;32m| 2.\033[0m \033[1;37mRemover Livro                     \033[1;32m|\033[0m")
            print("\033[1;32m| 3.\033[0m \033[1;37mBuscar Livro                      \033[1;32m|\033[0m")
            print("\033[1;32m| 4.\033[0m \033[1;37mOrdenar Livros                    \033[1;32m|\033[0m")
            print("\033[1;32m| 5.\033[0m \033[1;37mDesfazer Ação                     \033[1;32m|\033[0m")
            print("\033[1;32m| 6.\033[0m \033[1;37mSair                              \033[1;32m|\033[0m")
            print(borda_inferior)
            opcao = self.validar_entrada("\033[1;33mEscolha uma opção: \033[0m", 'str')
            if opcao == '1':
                self.adicionar_livro()
            elif opcao == '2':
                self.remover_livro()
            elif opcao == '3':
                self.buscar_livro()
            elif opcao == '4':
                self.ordenar_livros()
            elif opcao == '5':
                self.desfazer_acao()
            elif opcao == '6':
                print("Saindo do sistema...")
                break
            else:
                print("\033[1;31mOpção inválida. Tente novamente.\033[0m")
            input("\n\033[1;36mPressione Enter para continuar...\033[0m")

if __name__ == "__main__":
    biblioteca = BibliotecaConsole()
    biblioteca.exibir_menu()
