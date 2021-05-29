// var socket_private = io.connect('http://' + document.domain);
//     socket_private.on( 'connect', function() {
//       socket_private.emit( 'my event', {
//         data: 'User Connected'
//       } )
//       var form = $('.msger-send-btn').on( 'submit', function( e ) {
//         e.preventDefault()
//         let user_name = $( 'input.username' ).val()
//         let user_input = $( 'input.message' ).val()
//         socket_private.emit( 'my event', {
//           user_name : user_name,
//           message : user_input
//         } )
//         $( 'input.message' ).val( '' ).focus()
//       } )
//     } )
//     socket_private.on( 'my response', function( msg ) {
//       console.log( msg )
//       if( typeof msg.user_name !== 'undefined' ) {
//         $( 'h3' ).remove()
//         $( 'div.message_holder' ).append( '<div><b style="color: #000">'+msg.user_name+'</b> '+msg.message+'</div>' )
//       }
//     })



//  https://codepen.io/sajadhsm/pen/odaBdd

const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const bottomArrov = get(".to_bottom_arrov")
const notificationUrl = "http://zasx.tmweb.ru/sounds/notification_new_message.mp3"

// const PERSON_IMG = 'url("https://sun9-44.userapi.com/impf/c626528/v626528545/26a76/3zGUYjAshtU.jpg?size=900x900&quality=96&sign=bef06132184dc40b6740b17468d4c699&type=album")';
const PERSON_IMG = 'url("' + get('.nav-avatar').src + '")';
// get(".msg-img").style.backgroundImage ||
// console.log(PERSON_IMG)
const PERSON_NAME = getCookie('username');
const socket = io.connect('http://' + document.domain);
const socket_private = io.connect('http://' + document.domain) // + '/private');
function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

window.addEventListener("load", function() {
  // setTimeout(function() {
    console.log(msgerChat.scrollHeight)
    console.log()
    msgerChat.scrollTo(pageXOffset, msgerChat.scrollHeight);
    let chat_with = get(".chat-with")
    chat_with.textContent = 'Chat with ' + window.location.pathname.split('/')[2]

    // msgerChat.scrollTo(1,0);
    // msgerChat.scrollTo(pageXOffset, msgerChat );
      // msgerChat.scrollBottom;
      // if (scrollPos < 1) {
      //     window.scrollTo(0,1);
      // }
  // });
    socket_private.emit('username', PERSON_NAME);
});

// socket_private.on( 'connect', function() {
//     socket_private.emit( 'direct message', {
//       data: 'User Connected to Direct messages'
//     })
// })

msgerForm.addEventListener("submit", event => {
    // console.log('socket_private', document.domain )

    event.preventDefault();
    const msgText = msgerInput.value;
    if (!msgText) return;
    // let user_name = PERSON_NAME
    let user_input = msgText
    socket_private.emit( 'direct message', {
        user_name : PERSON_NAME,
        to_user : window.location.pathname.split('/')[2],
        message : user_input
    })
    // $( msgText ).val( '' ).focus()
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);

  msgerInput.value = "";
});

function appendMessage(name, img, side, text) {
  // console.log(img)
  const msgHTML = `
    <div class="msg ${side}-msg">
      <span aria-label="Ответить" class="reply"></span>
      <div class="msg-img" style='background-image: ${img}'></div>
      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>
        <div class="msg-text">
          <p>${text}</p>
        </div>
      </div>
    </div>
  `;
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

const relyeMessage = document.querySelectorAll(".left-msg")


for (let i=0; i < relyeMessage.length; i++) {
  relyeMessage[i].addEventListener('click', replyToMessage)
}


function replyToMessage(event) {
  event = event || window.event;
  msgerChat.insertAdjacentHTML("beforeend", `
  ${event.target.outerHTML}
  `);
  // ${event.target.getAttribute("msgid")}
  msgerChat.scrollTop += 200;


  console.log(event.target.outerHTML)
  // console.log(event.target.getAttribute("msgid"))
}


socket_private.on( 'direct message response', function( msg ) {
    // console.log( msg.user_name, PERSON_IMG, "left", msg.message)
    // console.log(msg)
    if( typeof msg !== 'undefined' && msg.sender != PERSON_NAME && (window.location.pathname.split('/')[2] == msg.sender) ) {
      appendMessage(msg.sender, PERSON_IMG, "left", msg.text)
      playSound(notificationUrl)
    } else if (typeof msg !== 'undefined' && msg.sender != PERSON_NAME) {
        item = get(`#${ msg.sender }`)
        console.log(item.children)
        const newMSG = `
          <span aria-label="Новое сообщение">
          &#128293;
          </span>
        `;
        item.children[0].insertAdjacentHTML("beforeend", newMSG);
    }
})

function playSound(url) {
  const audio = new Audio(url);
  audio.play();
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();
  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}

