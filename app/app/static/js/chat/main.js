// var socket = io.connect('http://' + document.domain);
//     socket.on( 'connect', function() {
//       socket.emit( 'my event', {
//         data: 'User Connected'
//       } )
//       var form = $('.msger-send-btn').on( 'submit', function( e ) {
//         e.preventDefault()
//         let user_name = $( 'input.username' ).val()
//         let user_input = $( 'input.message' ).val()
//         socket.emit( 'my event', {
//           user_name : user_name,
//           message : user_input
//         } )
//         $( 'input.message' ).val( '' ).focus()
//       } )
//     } )
//     socket.on( 'my response', function( msg ) {
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
// Icons made by Freepik from www.flaticon.com
const PERSON_IMG = 'url("' + get('.nav-avatar').src + '")';
// console.log(PERSON_IMG)
const PERSON_NAME = getCookie('username');
const socket = io.connect('http://' + document.domain + '/public');

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

window.addEventListener("load", function() {
  // setTimeout(function() {
    console.log(msgerChat.scrollHeight)
    msgerChat.scrollTo(pageXOffset, msgerChat.scrollHeight);
 
    // msgerChat.scrollTo(1,0);
    // msgerChat.scrollTo(pageXOffset, msgerChat );
      // msgerChat.scrollBottom;
      // if (scrollPos < 1) {
      //     window.scrollTo(0,1);
      // }
  // });
});

socket.on( 'connect', function() {
    socket.emit( 'my event', {
      data: 'User Connected'
    })
})
msgerForm.addEventListener("submit", event => {
    event.preventDefault();
    const msgText = msgerInput.value;
    if (!msgText) return;
    // let user_name = PERSON_NAME
    let user_input = msgText
    socket.emit( 'my event', {
        user_name : PERSON_NAME,
        message : user_input
    })
    // $( msgText ).val( '' ).focus()
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";
});

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style='background-image: ${img}'></div>
      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>
        <div class="msg-text"><p>${text}</p></div>
      </div>
    </div>
  `;
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

socket.on( 'my response', function( msg ) {
    // console.log( msg.user_name, PERSON_IMG, "left", msg.message)
    if( typeof msg.user_name !== 'undefined' && msg.user_name != PERSON_NAME ) {
        appendMessage(msg.user_name, PERSON_IMG, "left", msg.message)
    }
})


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
