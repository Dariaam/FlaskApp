
         let modal = document.getElementById("myModal");




         let span = document.getElementsByClassName("close")[0];

        modal.style.display = "block";


         span.onclick = function () {
             modal.style.display = "none";
         }


         window.onclick = function (event) {
             if (event.target == modal) {
                 modal.style.display = "none";
             }
         }

         document.getElementById('sendButton').addEventListener('click', async function () {
             let userInputElement = document.getElementById('userInput');
             if (userInputElement) {
                 let userInput = userInputElement.value;
                 if (userInput.trim() !== "") {
                     let chatMessages = document.getElementById('chatMessages');

                     let userMessage = document.createElement('div');
                     userMessage.className = 'user-message';
                     userMessage.textContent = userInput;
                     chatMessages.appendChild(userMessage);

                     let spinner = document.createElement('div');
                     spinner.className = 'spinner';
                     chatMessages.appendChild(spinner);

                     setTimeout(()=> {

                         chatMessages.removeChild(spinner);

                        
                    fetch('/api/function', { method: 'POST', 'body': userInput })
                    .then(response => response.json())
                    .then(data => {
                        let botMessageText = data.message;


                        let botMessage = document.createElement('div');
                        botMessage.className = 'bot-message';
                        botMessage.textContent = botMessageText;
                        chatMessages.appendChild(botMessage);


                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    })
                    .catch(error => console.error('Ошибка:', ошибка));
                         

                     }, 100000);

                     userInputElement.value = "";

                     chatMessages.scrollTop = chatMessages.scrollHeight;
                 }
             } else {
                 console.error('Error: userInput element not found.');
             }
         });

         document.querySelectorAll('.response-option').forEach(button => {
             button.addEventListener('click', function() {
                 let userInputElement = document.getElementById('userInput');
                 userInputElement.value = this.textContent;
                 document.getElementById('sendButton').click();
             });
         });


         setTimeout(() => {
         }, 2000);

