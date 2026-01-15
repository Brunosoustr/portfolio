import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_waste_data():
    """
    Analyzes the waste data from the Waste.xlsx file and generates visualizations.
    """
    try:
        # Load the dataset
        df = pd.read_excel("Projetos/Waste for Country/Waste.xlsx")

        # Set the style for the plots
        sns.set(style="whitegrid")

        # 1. Qual é a categoria alimentar que gera o maior desperdício total em toneladas e o maior prejuízo econômico?
        category_waste = df.groupby("Food Category")["Total Waste (Tons)"].sum().sort_values(ascending=False)
        category_loss = df.groupby("Food Category")["Economic Loss (Million $)"].sum().sort_values(ascending=False)

        # Plot for Total Waste by Food Category
        plt.figure(figsize=(10, 6))
        sns.barplot(x=category_waste.index, y=category_waste.values, palette="viridis")
        plt.title("Total de Desperdício por Categoria de Alimento")
        plt.xlabel("Categoria de Alimento")
        plt.ylabel("Total de Desperdício (Tons)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("Projetos/Waste for Country/total_waste_by_category.png")
        plt.close()

        # Plot for Economic Loss by Food Category
        plt.figure(figsize=(10, 6))
        sns.barplot(x=category_loss.index, y=category_loss.values, palette="plasma")
        plt.title("Prejuízo Econômico por Categoria de Alimento")
        plt.xlabel("Categoria de Alimento")
        plt.ylabel("Prejuízo Econômico (Milhões $)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("Projetos/Waste for Country/economic_loss_by_category.png")
        plt.close()

        # 2. Existe uma relação direta entre o total de resíduos gerados e a perda econômica?
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x="Total Waste (Tons)", y="Economic Loss (Million $)", hue="Food Category")
        plt.title("Relação entre Desperdício Total e Perda Econômica")
        plt.xlabel("Total de Desperdício (Tons)")
        plt.ylabel("Perda Econômica (Milhões $)")
        plt.tight_layout()
        plt.savefig("Projetos/Waste for Country/waste_vs_loss_correlation.png")
        plt.close()

        print("Análise de dados concluída e gráficos salvos com sucesso!")

        print_insights(df, category_waste, category_loss)

    except FileNotFoundError:
        print("Erro: O arquivo 'Waste.xlsx' não foi encontrado. Certifique-se de que ele está no diretório 'Projetos/Waste for Country/'.")
    except Exception as e:
        print(f"Ocorreu um erro durante a análise: {e}")

def print_insights(df, category_waste, category_loss):
    """
    Prints the insights from the analysis.
    """
    print("\n--- Insights da Análise ---")

    # 1. Qual é a categoria alimentar que gera o maior desperdício total em toneladas e o maior prejuízo econômico?
    print(f"\n1. Categoria com maior desperdício: '{category_waste.index[0]}' ({category_waste.iloc[0]:.2f} Tons)")
    print(f"   Categoria com maior prejuízo econômico: '{category_loss.index[0]}' (${category_loss.iloc[0]:.2f} Milhões)")

    # 2. Existe uma relação direta entre o total de resíduos gerados e a perda econômica?
    correlation = df["Total Waste (Tons)"].corr(df["Economic Loss (Million $)"])
    print(f"\n2. A correlação entre o total de resíduos e a perda econômica é: {correlation:.2f}")
    print("   Isso indica uma forte relação positiva entre as duas variáveis.")


if __name__ == "__main__":
    analyze_waste_data()
