import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from pathlib import Path

# Configuração de estilo para gráficos modernos e escuros
plt.style.use('dark_background')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# Cores modernas para o tema tech
colors = ['#6366f1', '#06b6d4', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']

def load_data():
    """Carrega os dados do arquivo Excel"""
    try:
        # Tentar diferentes caminhos possíveis
        paths = [
            'Plastic Pollution/Análise Plástico.xlsx',
            '../Plastic Pollution/Análise Plástico.xlsx',
            'Análise Plástico.xlsx'
        ]
        
        df = None
        for path in paths:
            if os.path.exists(path):
                df = pd.read_excel(path)
                print(f"Dados carregados de: {path}")
                break
        
        if df is None:
            print("Arquivo não encontrado. Gerando dados de exemplo...")
            df = generate_sample_data()
        
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        print("Gerando dados de exemplo...")
        return generate_sample_data()

def generate_sample_data():
    """Gera dados de exemplo se o arquivo não existir"""
    np.random.seed(42)
    
    # Tipos de plástico
    tipos_plastico = ['PE', 'PP', 'PS', 'PVC', 'PET']
    
    # Regiões oceânicas
    regioes = ['Pacífico Norte', 'Pacífico Sul', 'Atlântico Norte', 'Atlântico Sul', 
               'Índico', 'Ártico', 'Antártico']
    
    # Gerar dados
    n_samples = 500
    data = {
        'Data': pd.date_range('2020-01-01', periods=n_samples, freq='D'),
        'Regiao': np.random.choice(regioes, n_samples),
        'Tipo_Plastico': np.random.choice(tipos_plastico, n_samples, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
        'Latitude': np.random.uniform(-60, 60, n_samples),
        'Longitude': np.random.uniform(-180, 180, n_samples),
        'Peso_kg': np.random.lognormal(mean=3, sigma=1.5, size=n_samples),
        'Profundidade_m': np.random.uniform(0, 5000, n_samples)
    }
    
    df = pd.DataFrame(data)
    # Garantir que Peso seja positivo e razoável
    df['Peso_kg'] = np.abs(df['Peso_kg'])
    df['Peso_kg'] = df['Peso_kg'].clip(upper=1000)
    
    return df

def normalize_column_names(df):
    """Normaliza os nomes das colunas para facilitar o processamento"""
    df.columns = df.columns.str.strip()
    
    # Mapear possíveis variações de nomes
    column_mapping = {
        'Tipo de Plástico': 'Tipo_Plastico',
        'Tipo Plástico': 'Tipo_Plastico',
        'Tipo': 'Tipo_Plastico',
        'Peso (kg)': 'Peso_kg',
        'Peso': 'Peso_kg',
        'Região': 'Regiao',
        'Região do Oceano': 'Regiao',
        'Profundidade (m)': 'Profundidade_m',
        'Profundidade': 'Profundidade_m',
        'Lat': 'Latitude',
        'Lon': 'Longitude',
        'Long': 'Longitude'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Verificar se as colunas necessárias existem
    required_cols = ['Peso_kg', 'Regiao', 'Tipo_Plastico']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"Aviso: Colunas não encontradas: {missing_cols}")
        print(f"Colunas disponíveis: {list(df.columns)}")
    
    return df

def create_output_dir():
    """Cria o diretório de saída para os gráficos"""
    output_dir = Path('charts')
    output_dir.mkdir(exist_ok=True)
    return output_dir

def plot_weight_by_region(df, output_dir):
    """Gráfico 1: Peso total de plásticos por região"""
    if 'Regiao' not in df.columns or 'Peso_kg' not in df.columns:
        print("Colunas necessárias não encontradas para gráfico de peso por região")
        return
    
    weight_by_region = df.groupby('Regiao')['Peso_kg'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.barh(weight_by_region.index, weight_by_region.values, color=colors[:len(weight_by_region)])
    
    # Adicionar valores nas barras
    for i, (idx, val) in enumerate(weight_by_region.items()):
        ax.text(val + max(weight_by_region.values) * 0.01, i, 
                f'{val:.1f} kg', va='center', fontsize=10, color='white', fontweight='bold')
    
    ax.set_xlabel('Peso Total (kg)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Região Oceânica', fontsize=12, fontweight='bold')
    ax.set_title('Distribuição de Peso de Plásticos por Região Oceânica', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'peso_por_regiao.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0f', edgecolor='none')
    plt.close()
    print(f"✓ Gráfico salvo: {output_dir / 'peso_por_regiao.png'}")

def plot_plastic_types_by_region(df, output_dir):
    """Gráfico 2: Tipos de plásticos predominantes por região"""
    if 'Regiao' not in df.columns or 'Tipo_Plastico' not in df.columns:
        print("Colunas necessárias não encontradas para gráfico de tipos por região")
        return
    
    # Criar tabela cruzada
    cross_tab = pd.crosstab(df['Regiao'], df['Tipo_Plastico'])
    
    fig, ax = plt.subplots(figsize=(14, 8))
    cross_tab.plot(kind='barh', stacked=True, ax=ax, color=colors[:len(cross_tab.columns)])
    
    ax.set_xlabel('Quantidade de Observações', fontsize=12, fontweight='bold')
    ax.set_ylabel('Região Oceânica', fontsize=12, fontweight='bold')
    ax.set_title('Distribuição de Tipos de Plástico por Região', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(title='Tipo de Plástico', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'tipos_por_regiao.png', dpi=300, bbox_inches='tight',
                facecolor='#0a0a0f', edgecolor='none')
    plt.close()
    print(f"✓ Gráfico salvo: {output_dir / 'tipos_por_regiao.png'}")

def plot_plastic_types_distribution(df, output_dir):
    """Gráfico 3: Distribuição geral de tipos de plástico"""
    if 'Tipo_Plastico' not in df.columns:
        print("Coluna Tipo_Plastico não encontrada")
        return
    
    type_counts = df['Tipo_Plastico'].value_counts()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Gráfico de barras
    bars = ax1.bar(type_counts.index, type_counts.values, color=colors[:len(type_counts)])
    ax1.set_xlabel('Tipo de Plástico', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Frequência', fontsize=12, fontweight='bold')
    ax1.set_title('Frequência de Tipos de Plástico', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    # Gráfico de pizza
    wedges, texts, autotexts = ax2.pie(type_counts.values, labels=type_counts.index, 
                                       autopct='%1.1f%%', colors=colors[:len(type_counts)],
                                       startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax2.set_title('Distribuição Percentual de Tipos de Plástico', 
                  fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'distribuicao_tipos.png', dpi=300, bbox_inches='tight',
                facecolor='#0a0a0f', edgecolor='none')
    plt.close()
    print(f"✓ Gráfico salvo: {output_dir / 'distribuicao_tipos.png'}")

def plot_geographic_heatmap(df, output_dir):
    """Gráfico 4: Mapa de calor geográfico"""
    if 'Latitude' not in df.columns or 'Longitude' not in df.columns or 'Peso_kg' not in df.columns:
        print("Colunas geográficas não encontradas")
        return
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Criar scatter plot com tamanho e cor baseados no peso
    scatter = ax.scatter(df['Longitude'], df['Latitude'], 
                        c=df['Peso_kg'], s=df['Peso_kg']*2, 
                        cmap='viridis', alpha=0.6, edgecolors='white', linewidth=0.5)
    
    ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
    ax.set_title('Distribuição Geográfica de Plásticos nos Oceanos', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Adicionar colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Peso (kg)', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'mapa_calor_geografico.png', dpi=300, bbox_inches='tight',
                facecolor='#0a0a0f', edgecolor='none')
    plt.close()
    print(f"✓ Gráfico salvo: {output_dir / 'mapa_calor_geografico.png'}")

def plot_temporal_analysis(df, output_dir):
    """Gráfico 5: Análise temporal (se houver coluna de data)"""
    date_cols = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower() or 'Data' in col]
    
    if not date_cols:
        print("Coluna de data não encontrada, pulando análise temporal")
        return
    
    date_col = date_cols[0]
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    
    if len(df) == 0:
        print("Sem dados válidos de data")
        return
    
    # Agrupar por mês
    df['Mes'] = df[date_col].dt.to_period('M')
    monthly_weight = df.groupby('Mes')['Peso_kg'].sum()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(monthly_weight.index.astype(str), monthly_weight.values, 
            marker='o', linewidth=2.5, markersize=8, color=colors[0])
    ax.fill_between(range(len(monthly_weight)), monthly_weight.values, alpha=0.3, color=colors[0])
    
    ax.set_xlabel('Mês', fontsize=12, fontweight='bold')
    ax.set_ylabel('Peso Total (kg)', fontsize=12, fontweight='bold')
    ax.set_title('Variação Temporal do Peso de Plásticos', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'analise_temporal.png', dpi=300, bbox_inches='tight',
                facecolor='#0a0a0f', edgecolor='none')
    plt.close()
    print(f"✓ Gráfico salvo: {output_dir / 'analise_temporal.png'}")

def plot_depth_analysis(df, output_dir):
    """Gráfico 6: Análise de profundidade vs peso"""
    if 'Profundidade_m' not in df.columns or 'Peso_kg' not in df.columns:
        print("Colunas de profundidade não encontradas")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Scatter plot
    ax1.scatter(df['Profundidade_m'], df['Peso_kg'], alpha=0.6, 
               c=df['Profundidade_m'], cmap='plasma', s=50)
    ax1.set_xlabel('Profundidade (m)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Peso (kg)', fontsize=12, fontweight='bold')
    ax1.set_title('Relação entre Profundidade e Peso', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Box plot por faixa de profundidade
    df['Faixa_Profundidade'] = pd.cut(df['Profundidade_m'], 
                                      bins=[0, 500, 1000, 2000, 5000, float('inf')],
                                      labels=['0-500m', '500-1000m', '1000-2000m', '2000-5000m', '>5000m'])
    
    df_box = df.dropna(subset=['Faixa_Profundidade'])
    if len(df_box) > 0:
        df_box.boxplot(column='Peso_kg', by='Faixa_Profundidade', ax=ax2)
        ax2.set_xlabel('Faixa de Profundidade', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Peso (kg)', fontsize=12, fontweight='bold')
        ax2.set_title('Distribuição de Peso por Faixa de Profundidade', 
                     fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, linestyle='--')
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'analise_profundidade.png', dpi=300, bbox_inches='tight',
                facecolor='#0a0a0f', edgecolor='none')
    plt.close()
    print(f"✓ Gráfico salvo: {output_dir / 'analise_profundidade.png'}")

def main():
    """Função principal"""
    print("=" * 60)
    print("GERADOR DE GRÁFICOS - ANÁLISE DE POLUIÇÃO POR PLÁSTICOS")
    print("=" * 60)
    
    # Carregar dados
    print("\n[1/7] Carregando dados...")
    df = load_data()
    print(f"   Total de registros: {len(df)}")
    print(f"   Colunas: {list(df.columns)}")
    
    # Normalizar nomes das colunas
    print("\n[2/7] Normalizando colunas...")
    df = normalize_column_names(df)
    
    # Criar diretório de saída
    print("\n[3/7] Criando diretório de saída...")
    output_dir = create_output_dir()
    
    # Gerar gráficos
    print("\n[4/7] Gerando gráfico: Peso por Região...")
    plot_weight_by_region(df, output_dir)
    
    print("\n[5/7] Gerando gráfico: Tipos de Plástico por Região...")
    plot_plastic_types_by_region(df, output_dir)
    
    print("\n[6/7] Gerando gráfico: Distribuição de Tipos...")
    plot_plastic_types_distribution(df, output_dir)
    
    print("\n[7/7] Gerando gráfico: Mapa Geográfico...")
    plot_geographic_heatmap(df, output_dir)
    
    print("\n[8/8] Gerando gráfico: Análise Temporal...")
    plot_temporal_analysis(df, output_dir)
    
    print("\n[9/9] Gerando gráfico: Análise de Profundidade...")
    plot_depth_analysis(df, output_dir)
    
    print("\n" + "=" * 60)
    print("✓ TODOS OS GRÁFICOS FORAM GERADOS COM SUCESSO!")
    print(f"✓ Localização: {output_dir.absolute()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
