from fastapi import APIRouter, Request
from app.utils.huggingface import query_model
from app.services.account_service import get_account_balance, get_transaction_history
from app.services.transfer_service import send_money
from app.services.deposit_service import get_user_deposit, calculate_interest
from app.services.product_service import get_product_description
from app.services.auth_service import check_user_password

router = APIRouter()

user_sessions = {}         # {"김민지": True}
pending_transfers = {}     # {"김민지": {"from_id": ..., "to_name": ..., "amount": ...}}

@router.post("/chat")
async def handle_chat(request: Request):
    data = await request.json()
    user_input = data.get("text")

    # 1. 인텐트 + 슬롯 추출
    intent = query_model("intent", {"inputs": user_input})[0]["label"]
    slot_result = query_model("slot", {"inputs": user_input})

    # 2. login_user 인텐트만 인증 없이 허용
    if intent == "login_user":
        name, password = extract_user_auth_info(slot_result)
        if check_user_password(name, password):
            user_sessions[name] = True
            response_text = f"{name}님, 인증이 완료되었습니다. 무엇을 도와드릴까요?"
        else:
            response_text = "비밀번호가 틀렸습니다. 다시 입력해주세요."
        return simplify_response(response_text)

    # 3. 인증되지 않은 사용자는 모든 서비스 차단
    user_name = get_authenticated_user()
    if not user_name:
        return simplify_response("먼저 로그인해주세요. 이름과 비밀번호를 입력해주세요.")

    # 4. 인텐트별 처리
    try:
        if intent == "check_balance":
            account_id = extract_account_id(slot_result)
            balance = get_account_balance(account_id)
            response_text = f"현재 잔액은 {balance}원입니다."

        elif intent == "check_transaction_history":
            account_id, start_date, end_date = extract_transaction_slots(slot_result)
            records = get_transaction_history(account_id, start_date, end_date)
            response_text = f"{start_date}부터 {end_date}까지의 거래 내역은 {records}입니다."

        elif intent == "send_money":
            from_id, to_name, amount, pw = extract_transfer_slots(slot_result)

            if not pw:
                pending_transfers[user_name] = {
                    "from_id": from_id, "to_name": to_name, "amount": amount
                }
                response_text = f"{to_name}님께 {amount}원을 송금할까요? 비밀번호와 함께 말씀해주세요."
            else:
                if not check_user_password(user_name, pw):
                    return simplify_response("비밀번호가 틀렸습니다. 다시 입력해주세요.")
                data = pending_transfers.pop(user_name, {
                    "from_id": from_id, "to_name": to_name, "amount": amount
                })
                response_text = send_money(data["from_id"], data["to_name"], data["amount"])

        elif intent == "check_deposit_status":
            account_id = extract_account_id(slot_result)
            status = get_user_deposit(account_id)
            response_text = status

        elif intent == "calculate_interest":
            account_id = extract_account_id(slot_result)
            interest = calculate_interest(account_id)
            response_text = f"현재까지 쌓인 이자는 {interest}원입니다."

        elif intent in ["get_deposit_product_info", "get_savings_product_info", "get_loan_product_info"]:
            product_type = intent.split("_")[1]
            product_info = get_product_description(product_type)
            response_text = product_info

        else:
            response_text = "죄송해요, 무슨 말씀이신지 잘 모르겠어요."

        return simplify_response(response_text)

    except Exception as e:
        return {"error": str(e)}

# -------------------------
# 🔧 보조 함수들
# -------------------------

def is_authenticated():
    return get_authenticated_user() is not None

def get_authenticated_user():
    for name, status in user_sessions.items():
        if status:
            return name
    return None

def simplify_response(text: str):
    simplified = query_model("easy", {"inputs": text})
    return {"simplified": simplified[0]["generated_text"], "raw": text}

def extract_user_auth_info(slots):
    name, password = "", ""
    for slot in slots:
        if slot["entity_group"] == "user_name":
            name = slot["word"]
        elif slot["entity_group"] == "password":
            password = slot["word"]
    return name, password

def extract_account_id(slots):
    for slot in slots:
        if slot["entity_group"] == "account_id":
            return int(slot["word"].replace("#", ""))
    return 1

def extract_transaction_slots(slots):
    account_id, start_date, end_date = 1, None, None
    for slot in slots:
        if slot["entity_group"] == "start_date":
            start_date = slot["word"]
        elif slot["entity_group"] == "end_date":
            end_date = slot["word"]
        elif slot["entity_group"] == "account_id":
            account_id = int(slot["word"].replace("#", ""))
    return account_id, start_date or "2023-01-01", end_date or "2023-12-31"

def extract_transfer_slots(slots):
    from_id, to_name, amount, password = 1, "", 0, ""
    for slot in slots:
        if slot["entity_group"] == "receiver_name":
            to_name = slot["word"]
        elif slot["entity_group"] == "amount":
            amount = int(''.join(filter(str.isdigit, slot["word"])))
        elif slot["entity_group"] == "account_id":
            from_id = int(slot["word"].replace("#", ""))
        elif slot["entity_group"] == "password":
            password = slot["word"]
    return from_id, to_name, amount, password
