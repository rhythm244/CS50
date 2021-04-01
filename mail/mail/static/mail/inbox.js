document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // Add event listener to the form
  document.querySelector("#compose-form").addEventListener("submit", send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

//--------------ฟังก์ชั่นที่เอา csrf token มา---------------------------
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
//--------------จบ getCookie---------------------------
const csrftoken = getCookie('csrftoken');

function send_email(event) {
  // Modifies the default beheavor so it doesn't reload the page after submitting.
  event.preventDefault();

  // Get the required fields.
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  // Send the data to the server.
  fetch('/emails', {
    method: 'POST',
    headers:{
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      load_mailbox("sent", result);
      console.log(result);
      console.log(csrftoken);
  }).catch((error) => console.log(error));
}
 
function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) 
{
  // Show the mailbox and hide other views
  // document.querySelector('#emails-view').style.display = 'inline-block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    //fetch ข้อมูลมาจาก back-end โดยใช้ภาษา python
    fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => 
    {
      //create parent
      show_emails(emails)    

    })
    .catch((error) => console.error(error));
};

//show email in format
function show_emails(emails)
{
  var email_view = document.querySelector('#emails-view')
  //จะใช้ forEach หรือ for หรือ loop อะไรก็ได้
  
  emails.forEach((item) => 
  {
    const main = document.createElement("div");
    const sender = document.createElement('h6')
    const subject = document.createElement("h6");
    // const body = document.createElement("h6");
    const timestamp = document.createElement("h6");
    
    //ทำการเพิ่ม class ชื่อว่า mail ให้กับ element f แล้วค่อยไปแต่ง css เอา
    main.classList.add('mail') // add class ให้ main
    timestamp.classList.add('right')
    subject.classList.add('center')

    // main.innerHTML = `<strong>FORM: </strong> ${item["sender"]}`;
    sender.innerHTML = `<strong>${item["sender"]}</strong> `;
    subject.innerHTML = `${item["subject"]}`;
    // body.innerHTML = item["body"];
    timestamp.innerHTML = `<strong></strong> ${item["timestamp"]}`;

    email_view.appendChild(main);
    main.appendChild(sender);
    main.appendChild(subject);
    // main.appendChild(body);
    main.appendChild(timestamp);

    main.addEventListener('click', () => view_email());
  });
}

function view_email()
{
  return console.log("test");
}
