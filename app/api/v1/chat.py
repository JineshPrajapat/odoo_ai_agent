from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest
from app.api.response import success_response, error_response
from app.workflow.engine import WorkflowEngine
from app.core.database import get_db
from app.odoo.auth import OdooAuthService

router = APIRouter(prefix="/chat", tags=["agent"])

@router.post("/agent")
def test_agent(
    payload: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Test endpoint for AI → Odoo execution.
    """
    print("recived payload", payload)
    ODOO_UID = OdooAuthService().authenticate()

    response = WorkflowEngine().run(
        user_input=payload.message,
        odoo_uid=ODOO_UID,
    )

    return {
        "success": True,
        "state": "",
        "status_code": 200,
        "message": "Request processed successfully",
        "data": response
    }


# @router.get("/secure")
# def secure_endpoint(request: Request):
#     user_id = getattr(request.state, "user_id", None)
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Unauthorized")

#     return {"message": "Access granted", "user_id": user_id}

    # return {
    #         "status": "success",
    #         "status_code": 200,
    #         "message": "Request processed successfully",
    #         "data": {
    #             "version": "1.0",
    #             "summary": {
    #             "text": "Here are multiple example blocks for UI testing."
    #             },
    #             "blocks": [
    #             {
    #                 "type": "table",
    #                 "title": "User List",
    #                 "data": {
    #                 "columns": ["ID", "Name", "Email"],
    #                 "rows": [
    #                     ["1", "Alice", "alice@example.com"],
    #                     ["2", "Bob", "bob@example.com"],
    #                     ["3", "Charlie", "charlie@example.com"]
    #                 ]
    #                 }
    #             },
    #             {
    #                 "type": "list",
    #                 "title": "Top Cities",
    #                 "data": {
    #                 "items": ["New York", "London", "Tokyo", "Delhi"]
    #                 }
    #             },
    #             {
    #                 "type": "record",
    #                 "title": "Server Info",
    #                 "data": {
    #                 "Server Name": "ProdServer-01",
    #                 "Status": "Running",
    #                 "Uptime": "72 hours"
    #                 }
    #             },
    #             {
    #                 "type": "chart",
    #                 "title": "Sales by Month",
    #                 "data": {
    #                 "chartType": "bar",
    #                 "labels": ["Jan", "Feb", "Mar", "Apr"],
    #                 "values": [12000, 15000, 13000, 17000]
    #                 }
    #             },
    #             {
    #                 "type": "table",
    #                 "title": "Products",
    #                 "data": {
    #                 "columns": ["Product", "Category", "Price"],
    #                 "rows": [
    #                     ["Laptop", "Electronics", "$1200"],
    #                     ["Shoes", "Footwear", "$80"],
    #                     ["Coffee Mug", "Kitchen", "$15"]
    #                 ]
    #                 }
    #             },
    #             {
    #                 "type": "list",
    #                 "title": "Pending Tasks",
    #                 "data": {
    #                 "items": ["Finish report", "Review PR", "Send invoices"]
    #                 }
    #             },
    #             {
    #                 "type": "record",
    #                 "title": "User Profile",
    #                 "data": {
    #                 "Name": "David Lee",
    #                 "Email": "david.lee@example.com",
    #                 "Role": "Admin",
    #                 "Last Login": "2025-12-25 10:15 AM"
    #                 }
    #             },
    #             {
    #                 "type": "chart",
    #                 "title": "Website Traffic",
    #                 "data": {
    #                 "chartType": "line",
    #                 "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    #                 "values": [120, 150, 180, 170, 200]
    #                 }
    #             },
    #             {
    #                 "type": "table",
    #                 "title": "Employee Attendance",
    #                 "data": {
    #                 "columns": ["Employee", "Present Days", "Absent Days"],
    #                 "rows": [
    #                     ["Alice", 20, 2],
    #                     ["Bob", 18, 4],
    #                     ["Charlie", 22, 0]
    #                 ]
    #                 }
    #             },
    #             {
    #                 "type": "list",
    #                 "title": "Notifications",
    #                 "data": {
    #                 "items": ["New message from HR", "System update available", "Meeting at 3 PM"]
    #                 }
    #             }
    #             ],
    #             "meta": {
    #             "status": "success",
    #             "empty": False
    #             }
    #         }
    #         }
