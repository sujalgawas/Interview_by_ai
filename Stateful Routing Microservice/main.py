from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from episodic_memory import episodic
from state import class_state

#base model for query
class Query_model(BaseModel):
    user_token : int
    message : str    

app = FastAPI()

#defining data globally
chat_history = {}

def check_valid_user(user_token):
    """verify user using auth and database

    Args:
        user_token (id): JWT token generated (refreshed 7 days)

    Raises:
        HTTPException: user is authorized but not in database

    Returns:
        boolean : True or False depended upon the user is a authorized user
    """

    #user = admin_auth(token)
    #uid = user['uid']
    #if not uid
    #   return False    
    #try:
    #    user in database
    #except
    
    return True

@app.post('/chat/{session_id}')
async def chatmessage(query_model:Query_model,session_id:str):
    user_token = query_model.user_token  
    input_str = query_model.message
    session_id = session_id
    
    #function to validate user on every query
    if not check_valid_user(user_token):
        raise HTTPException(status_code = 401,detail="user is unauthorized")

    #checking if string is only consist of spaces
    if not input_str or not input_str.strip():
        return {"message":"Please Enter valid message","session_id":session_id,"state":"GENERAL_STATE"}
    
    
    episodic_mem = episodic(memory=chat_history,current_data=current_data)
    memory_count = episodic_mem.get_memory_count()
     
    State = class_state(memory=chat_history,current_data=current_data)
    
    order_id, state = State.check_return()
    
    if order_id == False and state == "REFUND_STATE":        
        current_data = {"session_id":session_id,"reponse":"Can you enter order id please","memory_count":memory_count+1,"state":state},201
    elif order_id != False and state == "REFUND_STATE":
        #calls another tools for the checking refund validity
        
        current_data = {"session_id":session_id,"reponse":"We have you order id we will check what we can do","memory_count":memory_count,"state":state},201
    
    if not current_data:
        #current_reponse will be replaced by llm or smart assistance
        current_reponse = "hi!"
        
        current_data = {"session_id":session_id,"reponse":current_reponse,"memory_count":memory_count+1,"state":state}
    
    #check_session function to check if the data exists
    check_session = episodic_mem.check_session()
    
    #updating the memory
    updating_memo = episodic_mem.updating_memory()
    
    if check_session and updating_memo:
        print("memory updated")
    
    return current_data,200
    
@app.get('/')
async def home():
    return "home page is working"