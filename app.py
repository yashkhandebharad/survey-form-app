import streamlit as st
import mysql.connector

# Function to connect to MySQL database using Streamlit secrets
def connect_to_db():
    db_host = st.secrets["mysql"]["db_host"]
    db_port = st.secrets["mysql"]["db_port"]
    db_user = st.secrets["mysql"]["db_user"]
    db_password = st.secrets["mysql"]["db_password"]
    db_name = st.secrets["mysql"]["db_name"]

    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        port=db_port
    )

# Function to insert data into the database
def insert_data(name, age, gender, salary, preferred_phone, budget):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = """
            INSERT INTO SurveyResponses (name, age, gender, salary, preferred_phone, budget)
            VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (name, age, gender, salary, preferred_phone, budget)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

# Streamlit app UI
def main():
    st.title("Survey Form")
    st.write("Please fill out the survey form below:")

    # Form fields
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    salary = st.number_input("Salary", min_value=0.0, step=1000.0)
    preferred_phone = st.selectbox("Which phone do you like?", ["iPhone", "Samsung", "OnePlus", "Other"])
    budget = st.number_input("How much are you ready to spend on the phone?", min_value=0.0, step=1000.0)

    if st.button("Submit"):
        if name.strip() == "":
            st.error("Name cannot be empty!")
        else:
            try:
                insert_data(name, age, gender, salary, preferred_phone, budget)
                st.success("Thank you for your response! Data has been saved.")
            except Exception as e:
                st.error(f"Error saving data: {e}")

if __name__ == "__main__":
    main()
