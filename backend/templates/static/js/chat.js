document.addEventListener("DOMContentLoaded", () => {


    const input = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");
    const messages = document.getElementById("chatMessages");


    if(!input || !sendBtn || !messages){
        return;
    }



    function addMessage(text, type){

        const div = document.createElement("div");

        div.className = `chat-message ${type}`;

        div.textContent = text;

        messages.appendChild(div);


        messages.scrollTop = messages.scrollHeight;

    }





    async function sendMessage(){


        const question = input.value.trim();


        if(!question){
            return;
        }



        addMessage(question, "user-message");


        input.value="";



        const loading = document.createElement("div");

        loading.className="chat-message ai-message loading";

        loading.textContent="Thinking...";


        messages.appendChild(loading);



        try{


            /*
                Temporary meeting id.
                Later we will load this dynamically
                from selected meeting.
            */

            const meetingId =
                localStorage.getItem("meeting_id") || 1;



            const response = await fetch("/chat/",{

                method:"POST",

                headers:{

                    "Content-Type":"application/json"

                },


                body:JSON.stringify({

                    meeting_id:Number(meetingId),

                    question:question

                })

            });



            const data = await response.json();



            loading.remove();



            addMessage(
                data.answer || "No answer received.",
                "ai-message"
            );


        }

        catch(error){


            loading.remove();


            addMessage(
                "Unable to connect with AI assistant.",
                "ai-message"
            );


            console.error(error);


        }


    }





    sendBtn.addEventListener(
        "click",
        sendMessage
    );



    input.addEventListener(
        "keypress",
        (event)=>{

            if(event.key==="Enter"){

                sendMessage();

            }

        }
    );


});

/* ================================
   CHAT MESSAGES
================================ */


