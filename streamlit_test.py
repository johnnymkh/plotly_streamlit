import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st



df=pd.read_csv('https://raw.githubusercontent.com/johnnymkh/plotly_streamlit/refs/heads/main/health.csv')
# original dataset cleaned using Data Wrangler

# reorder column for readability
col_order = ['Town', 'Area',
             'Total number of care centers', 'Total number of first aid centers', 
             'Existence of nearby care centers - exists', 'Existence of health resources - exists', 'Existence of a first aid center - exists',
             'Existence of special needs care centers - exists', 'Existence of special needs care centers - does not exist',
             'Type and size of medical resources - Pharmacies', 'Type and size of medical resources - Medical Centers', 
             'Type and size of medical resources - Hospitals', 'Type and size of medical resources - Clinics',
             'Type and size of medical resources - Labs and Radiology',
             'Percentage of towns with special needs indiciduals - Without special needs', 'Percentage of towns with special needs indiciduals - With special needs',
             ]
df = df[col_order]


# shorten column names
df = df.rename(columns={'Type and size of medical resources - Pharmacies':'Pharmacies',
                        'Type and size of medical resources - Medical Centers':'Medical Centers',
                        'Type and size of medical resources - Hospitals':'Hospitals',
                        'Type and size of medical resources - Clinics':'Clinics',
                        'Type and size of medical resources - Labs and Radiology':'Labs and Radiology'})

### TITLE
st.title(':green[Health data] in Lebanon')
st.divider()


### FIGURE 1: HEATMAP
st.subheader(':green[Correlation Heatmap] of Medical Resources')
medical_columns = ['Pharmacies', 'Medical Centers', 'Hospitals', 'Clinics',  'Labs and Radiology']
medical_data = df[medical_columns]

# Calculate the correlation matrix
correlation_matrix = medical_data.corr()



fig1 = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    colorscale='Viridis'
))

# Title and labels
fig1.update_layout(
    xaxis_title='Medical Resources',
    yaxis_title='Medical Resources'
)

# Display on streamlit
st.write(fig1)
st.divider()

st.subheader('Number of :green[Medical Resources] (by type) :green[per Area]')
# Group by area and sum the number of medical resources 
grouped_data = df.groupby('Area').agg({'Pharmacies': 'sum',
                                       'Medical Centers':'sum',
                                       'Hospitals':'sum',
                                       'Clinics':'sum',
                                       'Labs and Radiology':'sum',
                                       'Town': 'nunique'
                                       }).reset_index()

# Create a stacked bar chart
fig2 = px.bar(
    grouped_data, 
    x='Area', 
    y=['Pharmacies', 
       'Medical Centers',
       'Hospitals',
       'Clinics',
       'Labs and Radiology'],
    labels={'value': 'Total Resources', 'Area': 'Area'},
    barmode='stack',
    color_discrete_sequence=px.colors.diverging.Spectral
)

fig2.update_layout(xaxis={'categoryorder':'total descending'})

st.write(fig2)
st.divider()

st.subheader(':green[Percentage] of Medical Resources by type')
st.caption('Across all Towns')

total_pharma = df['Pharmacies'].sum()
total_med = df['Medical Centers'].sum()
total_hospitals = df['Hospitals'].sum()
total_clinics = df['Clinics'].sum()
total_lar = df['Labs and Radiology'].sum()

dfpie = pd.DataFrame({'Type of resource':['Pharmacies', 'Medical Centers', 'Hospitals', 'Clinics', 'Labs and Radiology'],
                      'Total count':[total_pharma, total_med, total_hospitals, total_clinics, total_lar]})

fig3 = px.pie(data_frame=dfpie, names='Type of resource', values='Total count')
st.write(fig3)
st.divider()

st.subheader('Average Number of :green[Care Centers] by Percentage of Elderly*')


demography = pd.read_csv('https://raw.githubusercontent.com/johnnymkh/plotly_streamlit/refs/heads/main/demography.csv')
merged_df = pd.merge(df, demography, on='Town')

# remove data error (Trablous Elderly 99%)
merged_df_clean = merged_df.loc[merged_df['Town']!='Trablous ']

# average to have one value per unique percentage
averaged_df = merged_df_clean.groupby('Percentage of Eldelry - 65 or more years ')['Total number of care centers'].mean().reset_index()

fig4 = px.line(data_frame=averaged_df, x='Percentage of Eldelry - 65 or more years ', y='Total number of care centers',
                  labels={'Percentage of Eldelry - 65 or more years ':'Percentage of Elderly (65+)', 'Total number of care centers':'Average Number of Care Centers'})
st.write(fig4)
st.caption('*Trablous was removed from the dataset for this visualization due to a data error')
st.divider()

st.subheader('Number of :green[Medical Resources by Age Group]')

y_option = st.selectbox(
    "Type of Resource",
    ('Pharmacies', 'Medical Centers', 'Hospitals', 'Clinics', 'Labs and Radiology'))

options = st.multiselect(
    "By Age",
    ['Percentage of Youth - 15-24 years','Percentage of Eldelry - 65 or more years ']
)

fig5 = px.histogram(merged_df, x=options, y=y_option)
st.write(fig5)
st.caption('*Note to self: When selecting both Age categories, histogram should ideally be overlapping not stacking')
