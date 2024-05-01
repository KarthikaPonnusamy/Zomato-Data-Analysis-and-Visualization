import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
from PIL import Image
import openpyxl
import plotly.express as px
import numpy as np  





#config page
icon = Image.open("zomatohome.jpg")
st.set_page_config(page_title= "Zomato Data Analysis and Visualization",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded"
                   )

st.sidebar.header(":red[**Zomato Data Analysis**]")


#load dataset
df = pd.read_csv("zomato.csv")
#country code
df_country = pd.read_excel('Country-Code.xlsx')
#merge file
df1 = pd.merge(df,df_country,on="Country Code",how='left')

with st.sidebar:
    selected = option_menu("Menu", ["Home","Dashboard","Explore Data on Map","Summary"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-1px", "--hover-color": "#FF5A5F"},
                        "nav-link-selected": {"background-color": "#FF5A5F"}})
    

if selected == "Home":

    st.markdown("# :red[Zomato Data Analysis and Visualization]")
    
    col1,col2 = st.columns([2,2],gap="medium")
    with col1:
        st.markdown("##")
        st.image("zomatologo.jpg")
        text = """
                **Zomato** *is a popular restaurant discovery and food delivery service*. 
                 \n**Problem Statement:**
                *Data analysis on the platform's data could be used to gain insights into customer preferences and behavior, as well as identify trends in the restaurant industry*.
                \n**To perform the analysis various methodologies such as Data Exploration, Data Cleaning, Feature Selection And Deployment can be used. Additionally, various data visualization techniques like bar charts, line charts**.
                \n**Data visualization can be used to effectively communicate the insights from Zomato data analysis to a wide range of stakeholders, including restaurants, food industry players, and investors.**.
                """


        st.markdown(text, unsafe_allow_html=True)
        st.write("---")

    with col2:

        st.video("https://youtu.be/OBmp_hlnhD0")


#Dashborad
if selected == "Dashboard":

    Country = st.selectbox('Select Country',df1['Country'].unique())
    City = st.selectbox('Select City',df1['City'].unique())

    tab1,tab2=st.tabs(['Pie Chart analysis','Bar chart analysis'])
  

    with tab1:
     
        
        col1,col2 = st.columns([2,2],gap="small")

        #Distribution of Online Delivery
        with col1:
            
            
            
            online_delivery = df1.groupby(['Country','City','Has Online delivery']).size().reset_index(name='count')
            
            online_delivery = online_delivery[['Country','City','Has Online delivery','count']].sort_values(by=['count'],ascending=False)[:5]

            x=online_delivery.apply(lambda x: f"{x['City']} - { x['Has Online delivery'] }", axis=1)
            y = online_delivery['count']

            fig, ax = plt.subplots(figsize=(1, 1))
            ax.pie(y, labels=x, autopct='%1.1f%%', startangle=200,textprops={'fontsize': 2},pctdistance=0.85)
            ax.set_title('Distribution of Online Delivery by Top 5 City',fontsize=4)                    
            st.pyplot(fig)

        #Distribution of Rating Text
        with col2:
          
            filtered_data = df1[(df1['Country'] == Country) & (df1['City'] == City)]
            rating_counts = filtered_data['Rating text'].value_counts()
           
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=200,textprops={'fontsize': 7},pctdistance=0.85)
            ax.set_title(f'Distribution of Rating Text in {City}, {Country}',fontsize=6)
            st.pyplot(fig)


    with tab2:
        col3,col4 = st.columns([2,2],gap="medium")

        with col3:
         
            #Top cuisine in city based voting
            filtered_city = df1[df1['City'] == City]
            grouped_data1 = filtered_city.groupby('Cuisines')['Votes'].sum().reset_index().sort_values(by='Votes', ascending=False)
            top_cuisines = grouped_data1.head(5)

            plt.figure(figsize=(10, 6))
            sns.barplot(x='Votes', y='Cuisines', data=top_cuisines, palette='viridis')
            plt.xlabel('Votes')
            plt.ylabel('Cuisines')
            plt.title(f'Top 5 Cuisines  by Votes')
            plt.grid(axis='y')
            plt.tight_layout()           
            st.pyplot(plt)

        #Cities by Avg. Item Prices
        with col4:

            ax = df.groupby('City')['Average Cost for two'].mean().apply(lambda x: round(x, 0)).to_frame().reset_index().sort_values(by='Average Cost for two',
                                                                                        ascending=False)[:10].plot.bar(x='City',y='Average Cost for two',figsize=(15,8))
            ax.bar_label(container=ax.containers[0], color='Red')
            plt.title("Cities by Avg. Item Prices",fontsize=20)
            plt.ylabel("Avg Prices",fontsize=18)
            plt.xlabel("City",fontsize=18)
            st.pyplot(plt)



        #Aggregate rating Count
        rating = df1.groupby(['Aggregate rating','Rating color','Rating text']).size().reset_index().rename(columns={0:'Rating Count'})
        fig = px.bar(rating, x='Aggregate rating', y='Rating Count',
                                labels='Rating color',
                                title='Aggregate rating Count',
                                width=800, height=500)

    
        st.plotly_chart(fig)

        locality_counts = df1['Locality'].value_counts()

        fig = px.bar(df1,
                        title='No of restaurents',
                        x="Locality",
                        orientation='v',                        
                        color_continuous_scale=px.colors.sequential.Reds)
        st.plotly_chart(fig,use_container_width=True)


#Explore the currency on map
if selected == "Explore Data on Map":
    st.header("Explore the currency on map")
    fig = px.scatter_geo(df1, 
                        lat='Latitude', 
                        lon='Longitude', 
                        color='Currency', 
                        size='Votes',
                        hover_name='City',
                        title='Zomato listing ',
                        width=1000,
                        height=200,
                        color_continuous_scale='Hot'
                        )
    fig.update_geos(
                    resolution=50,
                    showcoastlines=True, coastlinecolor="RebeccaPurple",
                    showland=True, landcolor="LightGreen",
                    showocean=True, oceancolor="LightBlue",
                    showlakes=True, lakecolor="Blue",
                    showrivers=True, rivercolor="Blue"
                            )
    fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)



if selected == "Summary":
        
        st.markdown("## :red[Contact Us]")
        col1, col2 =st.columns([3,2],gap="medium")
        with col1:
            st.image("abc.png")
        with col2:
    
            name = "Data visualized by: Karthika P "
            mail = (f'{"Mail :"}  {"pkarthika923@gmail.com"}')
            social_media = {"GITHUB": "https://github.com/KarthikaPonnusamy ",
                            "LINKEDIN": "https://www.linkedin.com/in/karthika-p-863361277/"
                            }
            st.subheader(name)
            st.write(mail)
            
            cols = st.columns(len(social_media))
            for index, (platform, link) in enumerate(social_media.items()):
                cols[index].write(f"[{platform}]({link})")


        st.header("**Summary**")
        text = """
                - Created a dropdown to choose the country-specific data.
                - Cuisines are costly in India.
                - Filter based on the city.
                - There is no relation between cost and rating. Some of the best-rated restaurants are low on cost and vice versa.
                - The top rated restaurants seems to be getting better rating 
                - Restaurants rating is categorized - Not Rated/Average/Good/Very Good/Excellent
                """
        st.write(text, unsafe_allow_html=True)