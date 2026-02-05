from flask import Blueprint,jsonify, redirect,request , render_template, url_for
from rt_app import  db
from rt_app.models import Conversation,RoomUser
import datetime
from rt_app.forms import JoinChatForm
from rt_app  import csrf
from rt_app.gemini_service import translate_text,generate_medical_summary

main =  Blueprint("main",__name__)
translation_cache = {}
@main.route("/")
def home():
    form = JoinChatForm()
    return render_template("home.html",form=form)



def cache_translation(text,from_lang, to_lang):

    key = f"{from_lang}|{to_lang}|{text}"


    if key in translation_cache:
        return translation_cache[key]


    translated = translate_text(text,from_lang,to_lang)
    translation_cache[key] = translated

    return translated


@main.route("/join",methods=["POST"])
def join_chat():
    form = JoinChatForm()
    if form.validate_on_submit():
        print("redirecting to chat.html")

        room_user = RoomUser(
        room=form.room.data,
        role=form.role.data,
        language=form.language.data
    )
        db.session.add(room_user)
        db.session.commit()
        return redirect(url_for("main.chat",room=form.room.data,role=form.role.data,lang=form.language.data))

    print("validation failed") 
    return redirect(url_for("main.home"))

@main.route("/chat/<room>/<role>/<lang>")
def chat(room, role,lang):
    return render_template("chat.html",title=role.title(),room=room,role=role,lang=lang)

@main.route("/send_message",methods=["POST"])
@csrf.exempt
def send_message():
    data = request.get_json()
    print(data)

    role = data['role']
    room = data['room']
    text = data['text']
    fromlang = data['language']

    lang_mapper = {
            "en":"English",
           "hi":"Hindi",
           "es":"Spanish",
           "fr":"French"
           }
    
    if role.lower()  == "doctor":
        target = RoomUser.query.filter_by(room=room,role='patient').first()

    else:
        target  = RoomUser.query.filter_by(room=room,role='doctor').first()
    print(target.language)
    to_lang = lang_mapper[target.language]
    translated_text = cache_translation(text, fromlang, to_lang)

    # print(f"Translated Text : {translated_text}")
    conversation = Conversation(
            role=role,
            room=room,
            translated_text=translated_text,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
            )

    db.session.add(conversation)
    db.session.commit()
    return jsonify({"status":"sucess"}),201



@main.route("/messages/<room>",methods=["GET"])
def load_message(room):
    conversation = Conversation.query.filter_by(room=room).all()
    return jsonify(
            {
                "data": [{
                "role": c.role,
                "room": c.room,
                "translated_text": c.translated_text
                }
                for c in conversation
                ]
            }

            )


@main.route("/create_room",methods=["POST"])
@csrf.exempt
def create_room():
    data = request.get_json()
    print(data)
    role = data['role']
    room = data['room']
    lang = data['language']
    room_user = RoomUser(
        room=room,
        role=role,
        language=lang
    )
    db.session.add(room_user)
    db.session.commit()
    return jsonify({"status":"Success Created room"})


@main.route("/summary/<room>", methods=["GET"])
@csrf.exempt
def generate_summary(room):
    conversation = Conversation.query.filter_by(room=room).all()

    conversation_ = {
                "data": [{
                "role": c.role,
                "room": c.room,
                "translated_text": c.translated_text
                }
                for c in conversation
                ]
            }
 
    summary = generate_medical_summary(conversation_)


    return jsonify({"summary": summary})

