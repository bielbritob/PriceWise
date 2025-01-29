// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

let dropConnections = {};

function sendValue(value) {
  Streamlit.setComponentValue(value);
}

function onRender(event) {
  if (!window.rendered) {
    console.log("Event detail:", event.detail);
    const htmlContent = event.detail.args.html_content;
    console.log("HTML Content:", htmlContent);

    document.getElementById("app").innerHTML = htmlContent;

    const draggables = document.querySelectorAll('.draggable');
    const droppables = document.querySelectorAll('.droppable');

    console.log("Draggables:", draggables);
    console.log("Droppables:", droppables);

    draggables.forEach(draggable => {
      draggable.addEventListener('dragstart', (event) => {
        event.dataTransfer.setData('text', draggable.id);
      });
    });

    droppables.forEach(droppable => {
      droppable.addEventListener('dragover', (event) => {
        event.preventDefault();
        droppable.classList.add('over');
      });

      droppable.addEventListener('dragleave', () => {
        droppable.classList.remove('over');
      });

      droppable.addEventListener('drop', (event) => {
        event.preventDefault();
        droppable.classList.remove('over');

        const droppedItemId = event.dataTransfer.getData('text');
        const droppedItem = document.getElementById(droppedItemId);
        const droppedItemText = droppedItem.textContent;
        const zoneId = droppable.id;

        if (!dropConnections[zoneId]) {
          dropConnections[zoneId] = [];
        }

        if (dropConnections[zoneId].includes(droppedItemText)) {
          alert(`${droppedItemText} já foi adicionado!`);
          return;
        }

        dropConnections[zoneId].push(droppedItemText);

        let droppedItemsContainer = droppable.querySelector('.dropped-items');
        if (!droppedItemsContainer) {
          droppedItemsContainer = document.createElement('div');
          droppedItemsContainer.classList.add('dropped-items');
          droppable.appendChild(droppedItemsContainer);
        }

        droppedItemsContainer.innerHTML = dropConnections[zoneId]
          .map(item => `<p>${item}</p>`)
          .join('');

        droppedItem.remove();

        console.log("Drop connections:", dropConnections);

        // Envia os dados formatados com tipo e conteúdo
        const streamlitMsg = {
          type: 'drop-event',
          data: dropConnections
        };
        sendValue(streamlitMsg);
      });
    });
    // main.js
    const droppable = document.createElement('div');
    droppable.className = 'droppable-zone';
    droppable.innerHTML = `
      <div class="drop-instruction">
        <span>⬇️ Arraste os produtos aqui</span>
      </div>
      <div class="dropped-items"></div>
    `;
    window.rendered = true;
  }
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
Streamlit.setComponentReady();
Streamlit.setFrameHeight(500);