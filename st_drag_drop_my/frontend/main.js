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
        const zoneId = droppable.id;

        // Clona o item inteiro (com img e preço)
        const clone = droppedItem.cloneNode(true);
        clone.style.opacity = "0.8";
        clone.style.transform = "scale(0.95)";
        clone.draggable = false; // Impede re-arraste

        // Cria container do item dropado
        const droppedItemContainer = document.createElement('div');
        droppedItemContainer.className = 'dropped-item';
        droppedItemContainer.appendChild(clone);

        // Adiciona à zona
        let droppedItemsContainer = droppable.querySelector('.dropped-items');
        if (!droppedItemsContainer) {
          droppedItemsContainer = document.createElement('div');
          droppedItemsContainer.className = 'dropped-items';
          droppable.appendChild(droppedItemsContainer);
        }

        droppedItemsContainer.appendChild(droppedItemContainer);

        // Atualiza dados para Streamlit
        const itemData = {
          id: droppedItemId,
          text: clone.querySelector('span').innerText,
          price: clone.querySelector('.preco-produto').innerText,
          image: clone.querySelector('img').src
        };

        if (!dropConnections[zoneId]) dropConnections[zoneId] = [];
        dropConnections[zoneId].push(itemData);

        // Envia dados estruturados
        sendValue({
          type: 'drop-event',
          data: dropConnections
        });
      });
    });

    window.rendered = true;
  }
}

// No final do arquivo você deve ter:
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
Streamlit.setComponentReady();
Streamlit.setFrameHeight(500);
