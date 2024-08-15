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
lucro_mes_categoria = df.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()                                                                     


def main():
    
    st.title("Análise de Vendas")
    st.image("vendas.png")
    
    
    total_custo = (df["Custo"].sum()).astype(int)
    total_custo = total_custo.astype(str)
    total_custo = total_custo.replace(".",",")
    total_custo = "R$" + total_custo[:2] + "." + total_custo[2:5] + "."+ total_custo[5:]
    
    total_lucro = (df["Lucro"].sum()).astype(int)
    total_lucro = total_lucro.astype(str)
    total_lucro = total_lucro.replace(".",",")
    total_lucro = "R$" + total_lucro[:2] + "." + total_lucro[2:5] + "."+ total_lucro[5:]
    
    total_clientes = df["ID Cliente"].nunique()
    
    col1, col2, col3 = st.columns(3)

    with col1:
       st.metric("Total Custo", total_custo)

    with col2:
        st.metric("Total Lucro", total_lucro)

    with col3:
        st.metric("Total Clientes", total_clientes)
        
    col1, col2 = st.columns(2)
    fig = px.bar(produtos_vendidos_marca, x="Quantidade", y="Marca", orientation="h",
               title="Total produtos vendidos por Marca", text="Quantidade",
               width=300, height=400)
    col1.plotly_chart(fig)
    
    fig1 = px.pie(lucro_categoria, values="Lucro", names="Categoria",
               title="Lucro por categoria",
               width=350, height=350)
    col2.plotly_chart(fig1)
    
    fig2 = px.line(lucro_mes_categoria, x="mes_ano", y="Lucro",
                   title="Lucro", color="Categoria", width=600, height=500)
    st.plotly_chart(fig2)

if __name__=="__main__":
    main()
    
    

