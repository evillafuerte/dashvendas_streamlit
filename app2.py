import pandas as pd
import plotly_express as px
import streamlit as st

# Lendo as bases de dados
df_vendas = pd.read_excel("Vendas.xlsx")
df_produtos = pd.read_excel("Produtos.xlsx")

# Merge
df = pd.merge(df_vendas, df_produtos, how='left', on='ID Produto') 


# Criando colunas
df["Custo"] = df["Custo Unitário"] * df["Quantidade"]
df["Lucro"] = df["Valor Venda"] - df["Custo"]
df["mes_ano"]= df["Data Venda"].dt.to_period("M").astype(str)

#Agrupamentos
produtos_vendidos_marca = df.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()
lucro_categoria = df.groupby("Categoria")["Lucro"].sum().reset_index() 


def main():
    st.title("Análise de Vendas")
    st.image("vendas.png")

    total_custo = (df["Custo"].sum()).astype(str)
    total_custo = total_custo.replace(".",",")
    total_custo = "R$" + total_custo[:2] + "." + total_custo[2:5] + "."+ total_custo[5:] 


    total_lucro = (df["Lucro"].sum()).astype(str)
    total_lucro = total_lucro.replace(".",",")
    total_lucro = "R$" + total_lucro[:2] + "." + total_lucro[2:5] + "."+ total_lucro[5:]

    total_clientes = df["ID Cliente"].nunique() 


    # Exibindo os valores com estilo CSS para controlar o tamanho da fonte e evitar truncamento
    st.markdown(
        f"""
        <div style="font-size: 18px;">
            <span>Total Custo: {total_custo}</span> <br>
            <span>Total Lucro: {total_lucro}</span> <br>
            <span>Total Clientes: {total_clientes}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    fig = px.bar(produtos_vendidos_marca, x="Quantidade", y="Marca", orientation="h",
                 title="Total produtos vendidos por Marca", text="Quantidade",
                 width=300, height=400)
    col1.plotly_chart(fig)

    fig1 = px.pie(lucro_categoria, values="Lucro", names="Categoria",
                  title="Lucro por categoria",
                  width=350,  height=350)
    col2.plotly_chart(fig1)


if __name__=="__main__":
    main()