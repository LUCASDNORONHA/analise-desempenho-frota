import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


class PlotHist:
    def __init__(self, db, coluna, titulo='', rotulo_x='', rotulo_y='Frequência', cor=None):
        self.db = db
        self.coluna = coluna
        self.titulo = titulo or f'Distribuição de {coluna.capitalize()}'
        self.rotulo_x = rotulo_x or coluna
        self.rotulo_y = rotulo_y
        self.cor = cor or ['#C6D9F1', '#1B4965']
        sns.set_style("whitegrid")
        plt.rcParams.update({
            'font.size': 12,
            'font.family': 'DejaVu Sans',
            'axes.titlesize': 16,
            'axes.titleweight': 'bold'
        })

    # -------------------------------------------------------
    # AUXILIARES
    # -------------------------------------------------------
    def _adicionar_logo(self, fig):
        try:
            logo_path = '../assets/cruzeiro-do-sul-logo.png'
            logo = plt.imread(logo_path)
            imagebox = OffsetImage(logo, zoom=0.30)
            ab = AnnotationBbox(imagebox, (0.98, 0.02), frameon=False,
                                xycoords='figure fraction', box_alignment=(1, 0))
            fig.add_artist(ab)
        except FileNotFoundError:
            print("Logo não encontrado. Ignorando inserção de logo.")

    def _adicionar_fonte(self):
        plt.figtext(0.02, 0.01,
                    'Fonte: Base de dados da disciplina. Elaborado por Lucas Dias Noronha.',
                    ha='left', va='bottom', fontsize=10, color='gray')

    # -------------------------------------------------------
    # HISTOGRAMA
    # -------------------------------------------------------
    def plot_histograma(self, bins=10):
        dados = self.db[self.coluna].dropna()

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(dados, bins=bins, kde=True, color=self.cor[1], ax=ax, alpha=0.8, edgecolor=self.cor[0])

        media = dados.mean()
        mediana = dados.median()
        desvio = dados.std()

        ax.axvline(media, color=self.cor[0], linestyle='--', linewidth=2, label=f'Média = {media:.2f}')
        ax.axvline(mediana, color=self.cor[1], linestyle=':', linewidth=2, label=f'Mediana = {mediana:.2f}')

        ax.set_title(self.titulo, pad=20, color=self.cor[1])
        ax.set_xlabel(self.rotulo_x)
        ax.set_ylabel(self.rotulo_y)
        ax.legend(frameon=False, loc='upper right')

        # Caixa de resumo estatístico
        resumo = f"Média: {media:.2f}\nMediana: {mediana:.2f}\nDesvio-padrão: {desvio:.2f}"
        ax.text(0.02, 0.95, resumo, transform=ax.transAxes, fontsize=10,
                va='top', ha='left', color=self.cor[1], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5',
                          facecolor=self.cor[0], alpha=0.8, edgecolor='none'))

        sns.despine(ax=ax, top=True, right=True, left=True, bottom=False)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.tick_params(axis='x', length=0)
        ax.tick_params(axis='y', length=0)

        self._adicionar_fonte()
        self._adicionar_logo(fig)
        plt.tight_layout(rect=[0, 0.05, 1, 0.93])

        plt.savefig(f'../reports/figures/histograma_{self.coluna}.png',
                    dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.show()