import matplotlib.pyplot as plt
from typing import List, Dict

class Livro:
    def __init__(self, titulo: str, autor: str, genero: str, quantidade: int):
        self.titulo = titulo.title()
        self.autor = autor.title()
        self.genero = genero.title()
        self.quantidade = max(0, quantidade)  # Garante que não seja negativo
    
    def __str__(self):
        return f"📖 {self.titulo} | ✍️ {self.autor} | 🏷️ {self.genero} | 📊 {self.quantidade} unidades"
    
    def to_dict(self):
        """Converte o livro para dicionário para facilitar exportação"""
        return {
            'titulo': self.titulo,
            'autor': self.autor,
            'genero': self.genero,
            'quantidade': self.quantidade
        }

class Biblioteca:
    def __init__(self):
        self.livros: List[Livro] = []
    
    def cadastrar_livro(self) -> None:
        print("\n" + "="*50)
        print("📚 CADASTRO DE LIVRO")
        print("="*50)
        
        try:
            titulo = input("Título: ").strip()
            if not titulo:
                print("❌ Título é obrigatório!")
                return
            
            # Verifica se livro já existe
            if any(livro.titulo.lower() == titulo.lower() for livro in self.livros):
                print("❌ Já existe um livro com este título!")
                return
            
            autor = input("Autor: ").strip()
            genero = input("Gênero: ").strip()
            
            quantidade = int(input("Quantidade disponível: "))
            if quantidade < 0:
                print("❌ Quantidade não pode ser negativa!")
                return
            
            novo_livro = Livro(titulo, autor, genero, quantidade)
            self.livros.append(novo_livro)
            print(f"\n✅ '{titulo}' cadastrado com sucesso!")
            
        except ValueError:
            print("❌ Erro: Quantidade deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    def listar_livros(self) -> None:
        print("\n" + "="*50)
        print("📋 LISTA DE LIVROS")
        print("="*50)
        
        if not self.livros:
            print("📭 Nenhum livro cadastrado.")
            return
        
        # Ordena por título
        livros_ordenados = sorted(self.livros, key=lambda x: x.titulo)
        
        for i, livro in enumerate(livros_ordenados, 1):
            print(f"{i:2d}. {livro}")
        
        print(f"\n📊 Total: {len(self.livros)} livro(s) cadastrado(s)")
    
    def buscar_livro(self) -> None:
        print("\n" + "="*50)
        print("🔍 BUSCAR LIVRO")
        print("="*50)
        
        termo = input("Digite título, autor ou gênero: ").strip().lower()
        
        if not termo:
            print("❌ Termo de busca não pode estar vazio!")
            return
        
        encontrados = [
            livro for livro in self.livros 
            if termo in livro.titulo.lower() or 
               termo in livro.autor.lower() or 
               termo in livro.genero.lower()
        ]
        
        if encontrados:
            print(f"\n🎯 Encontrados {len(encontrados)} livro(s):")
            for i, livro in enumerate(encontrados, 1):
                print(f"{i}. {livro}")
        else:
            print("\n🔍 Nenhum livro encontrado com esse termo.")
    
    def remover_livro(self) -> None:
        print("\n" + "="*50)
        print("🗑️ REMOVER LIVRO")
        print("="*50)
        
        if not self.livros:
            print("📭 Nenhum livro cadastrado para remover.")
            return
        
        self.listar_livros()
        
        try:
            numero = int(input("\nNúmero do livro a remover (0 para cancelar): "))
            if numero == 0:
                return
            
            if 1 <= numero <= len(self.livros):
                livro_removido = self.livros.pop(numero - 1)
                print(f"✅ '{livro_removido.titulo}' removido com sucesso!")
            else:
                print("❌ Número inválido!")
                
        except ValueError:
            print("❌ Digite um número válido!")
    
    def estatisticas(self) -> None:
        print("\n" + "="*50)
        print("📊 ESTATÍSTICAS")
        print("="*50)
        
        if not self.livros:
            print("📭 Nenhum livro cadastrado.")
            return
        
        total_livros = sum(livro.quantidade for livro in self.livros)
        total_titulos = len(self.livros)
        
        # Estatísticas por gênero
        generos: Dict[str, int] = {}
        for livro in self.livros:
            generos[livro.genero] = generos.get(livro.genero, 0) + livro.quantidade
        
        print(f"📚 Total de exemplares: {total_livros}")
        print(f"📖 Total de títulos diferentes: {total_titulos}")
        print(f"🏷️ Gêneros cadastrados: {len(generos)}")
        
        if generos:
            print("\n📈 Distribuição por gênero:")
            for genero, quantidade in sorted(generos.items()):
                percentual = (quantidade / total_livros) * 100
                print(f"  • {genero}: {quantidade} ({percentual:.1f}%)")
    
    def gerar_grafico_generos(self) -> None:
        if not self.livros:
            print("\n📭 Não há livros cadastrados para gerar o gráfico.")
            return
        
        generos: Dict[str, int] = {}
        for livro in self.livros:
            generos[livro.genero] = generos.get(livro.genero, 0) + livro.quantidade
        
        # Ordena por quantidade (decrescente)
        generos_ordenados = dict(sorted(generos.items(), 
                                      key=lambda x: x[1], reverse=True))
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(generos_ordenados.keys(), generos_ordenados.values(), 
                      color=plt.cm.Set3(range(len(generos_ordenados))))
        
        plt.title("📊 Distribuição de Livros por Gênero", fontsize=14, fontweight='bold')
        plt.xlabel("Gênero")
        plt.ylabel("Quantidade de Livros")
        plt.xticks(rotation=45, ha='right')
        
        # Adiciona valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
        
        print("📈 Gráfico gerado com sucesso!")

def menu() -> None:
    biblioteca = Biblioteca()
    
    while True:
        print("\n" + "="*60)
        print("🏛️  SISTEMA DE BIBLIOTECA")
        print("="*60)
        print("1. 📚 Cadastrar novo livro")
        print("2. 📋 Listar todos os livros")
        print("3. 🔍 Buscar livro")
        print("4. 🗑️ Remover livro")
        print("5. 📊 Ver estatísticas")
        print("6. 📈 Gerar gráfico por gênero")
        print("7. 🚪 Sair")
        print("-"*60)
        
        opcao = input("Escolha uma opção (1-7): ").strip()
        
        opcoes = {
            '1': biblioteca.cadastrar_livro,
            '2': biblioteca.listar_livros,
            '3': biblioteca.buscar_livro,
            '4': biblioteca.remover_livro,
            '5': biblioteca.estatisticas,
            '6': biblioteca.gerar_grafico_generos,
            '7': lambda: None  # Para tratamento especial abaixo
        }
        
        if opcao == '7':
            print("\n👋 Obrigado por usar o Sistema de Biblioteca!")
            print("Até logo! 📚")
            break
        elif opcao in opcoes:
            opcoes[opcao]()
        else:
            print("❌ Opção inválida! Digite um número entre 1 e 7.")
        
        input("\n⏎ Pressione Enter para continuar...")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário!")
    except Exception as e:
        print(f"\n💥 Erro crítico: {e}")
