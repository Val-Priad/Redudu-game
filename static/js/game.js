MAKE_A_MOVE = "make-a-move";
USE_CARDS = "use-cards";
BEAT_CARDS = "beat-cards";
MOVE_CARDS = "move-cards";
TAKE_CARDS = "take-cards";
DEACTIVATE_CARDS = "deactivate-cards";

let gameState;

const warningSection =
    document.querySelector(".warning");
const loadingSection =
    document.querySelector(".loading-screen");

const one_row_section =
    document.querySelector(".one-row")
const player_section =
    document.querySelector(".player-field");
const game_data_section =
    document.querySelector(".game-data")

DECK = {
    '2C': 'Двійка треф', '2D': 'Двійка бубна', '2H': 'Двійка чирва',
    '2S': 'Двійка піка', '3C': 'Трійка треф', '3D': 'Трійка бубна',
    '3H': 'Трійка чирва', '3S': 'Трійка піка', '4C': 'Четвірка треф',
    '4D': 'Четвірка бубна', '4H': 'Четвірка чирва', '4S': 'Четвірка піка',
    '5C': "П'ятірка треф", '5D': "П'ятірка бубна", '5H': "П'ятірка чирва",
    '5S': "П'ятірка піка", '6C': 'Шістка треф', '6D': 'Шістка бубна',
    '6H': 'Шістка чирва', '6S': 'Шістка піка', '7C': 'Сімка треф',
    '7D': 'Сімка бубна', '7H': 'Сімка чирва', '7S': 'Сімка піка',
    '8C': 'Вісімка треф', '8D': 'Вісімка бубна', '8H': 'Вісімка чирва',
    '8S': 'Вісімка піка', '9C': "Дев'ятка треф", '9D': "Дев'ятка бубна",
    '9H': "Дев'ятка чирва", '9S': "Дев'ятка піка", '0C': 'Десятка треф',
    '0D': 'Десятка бубна', '0H': 'Десятка чирва', '0S': 'Десятка піка',
    'JC': 'Валет треф', 'JD': 'Валет бубна', 'JH': 'Валет чирва',
    'JS': 'Валет піка', 'QC': 'Дама треф', 'QD': 'Дама бубна',
    'QH': 'Дама чирва', 'QS': 'Дама піка', 'KC': 'Король треф',
    'KD': 'Король бубна', 'KH': 'Король чирва', 'KS': 'Король піка',
    'AC': 'Туз треф', 'AD': 'Туз бубна', 'AH': 'Туз чирва',
    'AS': 'Туз піка', 'X1': 'Чорний Джокер', 'X2': 'Червоний Джокер'
}

function showLoading() {
    loadingSection.classList.add('visible');
}
function hideLoading() {
    loadingSection.classList.remove('visible');
}


function insertToGameState(state) {
    if (typeof state !== 'object' || state === null) {
        console.error('Invalid state provided');
        return;
    }

    gameState = {...state};

    console.log('Game state updated:', gameState);
}

function updateGameState() {
    document.getElementById("enemy-1-name").textContent =
        gameState.player_name_dict.enemy_1_name;
    document.getElementById("enemy-2-name").textContent =
        gameState.player_name_dict.enemy_2_name;

    const enemy1Img =
        document.querySelector(".enemy-1-field img");
    const enemy2Img =
        document.querySelector(".enemy-2-field img");
    enemy1Img.src = `../static/img/${gameState.gifs_dict.enemy_1_gif}.gif`;
    enemy2Img.src = `../static/img/${gameState.gifs_dict.enemy_2_gif}.gif`;

    document.getElementById("qty-cards-enemy-1").textContent =
        `У стосі ще ${gameState.player_piles["Player 1"].length} карт`;
    document.getElementById("qty-cards-enemy-2").textContent =
        `У стосі ще ${gameState.player_piles["Player 2"].length} карт`;

    document.getElementById("enemy-1-hand").textContent =
        `У руці ${gameState.hands["Player 1"].length} карт`;
    document.getElementById("enemy-2-hand").textContent =
        `У руці ${gameState.hands["Player 2"].length} карт`;



    if (gameState.common_pile.length === 0) {
        document.querySelector(".deck").style.display = "none";
    } else {
        const deckField = document.querySelector(".deck p");
        deckField.textContent =
            `Залишилось карт ${gameState.common_pile.length}`;
    }

    document.getElementById("qty-cards-player").textContent =
        `У стосі ще ${gameState.player_piles["Player 3"].length} карт`;

    const playerTrump = gameState.player_trumps["Player 3"];
    const trumpInHand = gameState.hands["Player 3"].includes(playerTrump);
    document.getElementById("trump-player").textContent =
        trumpInHand ? `Ваш козир: ${DECK[playerTrump].toLowerCase()}`
            : "Ваш козир: невідомо";

    const enemy1Trump = gameState.player_trumps["Player 1"];
    const trumpInHandEn1 = gameState.hands["Player 1"].includes(enemy1Trump);
    document.getElementById("trump-enemy-1").textContent =
        trumpInHandEn1 ? DECK[gameState.player_trumps["Player 1"]].toLowerCase()
            : "невідомо";
    const enemy2Trump = gameState.player_trumps["Player 2"];
    const trumpInHandEn2 = gameState.hands["Player 2"].includes(enemy2Trump);
    document.getElementById("trump-enemy-2").textContent =
        trumpInHandEn2 ? DECK[gameState.player_trumps["Player 2"]].toLowerCase()
            : "невідомо";

    const deckTrump =
        document.querySelector(".deck p:nth-of-type(2)");
    deckTrump.textContent =
        `Козир ${DECK[gameState.common_trump].toLowerCase()}`;

    const commonTrumpInPlayerSection =
        document.getElementById("common-trump-player")
    commonTrumpInPlayerSection.textContent =
        `Загальний козир: ${DECK[gameState.common_trump].toLowerCase()}`;

    populateCards(".enemy-1-cards", gameState.hands["Player 1"]);
    populateCards(".enemy-2-cards", gameState.hands["Player 2"]);
    populateCards(".player-cards", gameState.hands["Player 3"]);

    const whoseTurn =
        document.getElementById("whose-turn");
    console.log(gameState.current_player);
    if ([1, 2].includes(gameState.current_player)) {
        whoseTurn.innerText =
            `Хід виконує ${gameState.player_name_dict[`enemy_${
                gameState.current_player}_name`]}`;
    } else {
        whoseTurn.innerText = "Ваша черга!";
    }

    const clearCardsInGame = [...gameState.cards_in_game.map(x => x[0])];
    populateCards(".cards-in-game", clearCardsInGame);
}

function populateCards(selector, cards) {
    const cardsContainer = document.querySelector(selector);
    cardsContainer.innerHTML = "";
    cards.forEach(card => {
        const cardElement =
            document.createElement("div");
        cardElement.className = "card";
        const cardImg =
            document.createElement("img");
        cardImg.src = `../static/img/cards/${card}.png`;
        cardImg.alt = card;

        cardElement.appendChild(cardImg);
        cardsContainer.appendChild(cardElement);
    });
}

function loadCards() {
    const deckShuffling =
        document.getElementById("deck-shuffling");
    const cardNames = Object.keys(DECK);


    deckShuffling.innerHTML = "";

    cardNames.forEach(card => {
        const cardElement =
            document.createElement("div");
        cardElement.classList.add("card-shuffling");
        cardElement.style.backgroundImage =
            `url('../static/img/cards/${card}.png')`;


        deckShuffling.appendChild(cardElement);
    });
}

function shuffleDeck() {
    const deck =
        document.getElementById("deck-shuffling");
    const cards = Array.from(deck.children);

    cards.forEach((card, index) => {
        const angle = Math.random() * 360;
        const x = Math.random() * 100 - 50;
        const y = Math.random() * 100 - 50;

        card.style.transform = `rotate(${angle}deg)`;
        card.style.top = `${y}px`;
        card.style.left = `${x}px`;

        setTimeout(() => {
            card.style.transform = "rotate(0deg)";
            card.style.top = "0px";
            card.style.left = "0px";
        }, 750 + index * 100);
    });
}


async function showLoadingScreen() {
    const loadingScreen =
        document.getElementById('loading-screen');
        showLoading()
        loadCards();
        await wait(3.5)
        shuffleDeck();
        setTimeout(() => {
            hideLoading()
            hideLoadingScreen();
            shuffleCards()
                .then(shuffledDeck => {
                    insertToGameState(shuffledDeck);
                    updateGameState();
                    startGame().catch(err => {
                        console.error('Failed to load game state:', err);
                    })
                })
                .catch(err => {
                    console.error('Failed to load game state:', err);
                });

        }, 8000);
}



function hideLoadingScreen() {
    const loadingScreen =
        document.getElementById('loading-screen');
    loadingScreen.style.display = 'none';
}

function shuffleCards() {
    return fetch('/game/shuffle')
        .then(res => {
            if (!res.ok) {
                throw new Error(`Http error! Status: ${res.status}`);
            }
            return res.json();
        })
        .catch(err => {
            console.error(err);
            throw err;
        });
}

function checkForWinner() {
    for (const player in gameState.hands) {
        if (gameState.hands[player].length === 0) {
            let num = parseInt(player.split(" ")[1], 10);
            if ([1, 2].includes(num)) {
                return gameState.player_name_dict[`enemy_${num}_name`]
            }
            else {
                return "gamer"
            }
        }
    }
    return null;
}

function AImove() {
    return fetch('/game/AImove', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({gameState}),
    })
        .then(res => {
            if (!res.ok) {
                throw new Error(`Http error! Status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            console.log('Response: ', data);
            insertToGameState(data);
        }).then(async () => {
                let player_num = gameState.current_player;
                if (player_num + 1 === 3) {
                    await wait(2)
                } else {
                    await wait(3)
                }
            }
        ).then(() => {
                updateGameState();
            }
        )
        .catch(error => {
            console.error('Error:', error);
        });
}

let gameHistory = [];

let previousGameState = null;

function showChanges() {
    const maxHistory = 4;
    const maxWordsPerLine = 9;

    if (
        previousGameState &&
        JSON.stringify(previousGameState) === JSON.stringify(gameState)
    ) {
        console.log("Немає змін у стані гри.");
        return;
    }

    previousGameState = JSON.parse(JSON.stringify(gameState));

    if (gameState.what_was_done) {
        const words = gameState.what_was_done.split(" ");
        const formattedLines = [];
        for (let i = 0; i < words.length; i += maxWordsPerLine) {
            formattedLines.push(words.slice(i, i + maxWordsPerLine).join(" "));
        }

        formattedLines.forEach(line => gameHistory.unshift(line));

        while (gameHistory.length > maxHistory) {
            gameHistory.pop();
        }
    }

    for (let i = 1; i <= maxHistory; i++) {
        const turnElement =
            document.getElementById(`previous-turn-${i}`);
        if (gameHistory[i - 1]) {
            turnElement.textContent = gameHistory[i - 1];
        } else {
            turnElement.textContent = '';
        }
    }

    const enemy1Cards
        = document.getElementById("qty-cards-enemy-1");
    const enemy2Cards
        = document.getElementById("qty-cards-enemy-2");
    const playerCards
        = document.getElementById("qty-cards-player");

    enemy1Cards.textContent =
        `У стосі ще ${gameState.player_piles["Player 1"].length} карт`;
    enemy2Cards.textContent =
        `У стосі ще ${gameState.player_piles["Player 2"].length} карт`;
    playerCards.textContent =
        `У стосі ще ${gameState.player_piles["Player 3"].length} карт`;

    const enemy1Hand
        = document.getElementById("enemy-1-hand");
    const enemy2Hand
        = document.getElementById("enemy-2-hand");

    enemy1Hand.textContent =
        `У руці ${gameState.hands["Player 1"].length} карт`;
    enemy2Hand.textContent =
        `У руці ${gameState.hands["Player 2"].length} карт`;


    const cardInGameField =
        document.querySelector(".card-in-game img");
    const lastCardEntry = gameState.cards_in_game.slice(-1)[0];

    if (lastCardEntry && lastCardEntry.card) {
        cardInGameField.src = `../static/img/cards/${lastCardEntry.card}.png`;
        cardInGameField.alt = lastCardEntry.card;
    }

}

function goBack() {
    const userConfirmed =
        confirm("Ви впевнені, що хочете завершити гру?")
    if (userConfirmed) {
        window.location.href = "/";
    }

}

function showUserButtons() {
    const playButtons =
        document.getElementsByClassName('play-button');
    let cardsInGame = gameState.cards_in_game;
    let curPlayer = gameState.current_player === 3;
    let canDisplayMakeAmove = cardsInGame.length === 0 && curPlayer;
    for (let i = 0; i < playButtons.length; i++) {
        let currentButtonIsUseCards =
            playButtons[i].id === USE_CARDS && curPlayer;
        let currentButtonIsMakeAmove =
            playButtons[i].id === MAKE_A_MOVE && curPlayer;
        let currentButtonIsDeactivate =
            playButtons[i].id === DEACTIVATE_CARDS && curPlayer;

        let currentButtonWorkOnlyWhenAttack =
            [BEAT_CARDS, TAKE_CARDS, MOVE_CARDS].includes(playButtons[i].id);

        if (currentButtonIsUseCards || currentButtonIsDeactivate) {
            playButtons[i].style.display = "none";
        } else if (currentButtonIsMakeAmove && !canDisplayMakeAmove) {
            playButtons[i].style.display = "none";
        } else if (currentButtonWorkOnlyWhenAttack && canDisplayMakeAmove) {
            playButtons[i].style.display = "none";
        } else {
            playButtons[i].style.display = "block";
        }
    }
}

function hideUserButtons() {
    const playButtons =
        document.getElementsByClassName('play-button');

    for (let i = 0; i < playButtons.length; i++) {
        playButtons[i].style.display = "none";
    }
}

function wait(s) {
    let ms = s * 1000
    return new Promise(resolve => setTimeout(resolve, ms));
}

function takeCards() {
    let cards_in_game = gameState.cards_in_game
    if (cards_in_game.length !== 0) {
        return fetch('/game/takeCards', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({gameState}),
        })
            .then(res => {
                if (!res.ok) {
                    throw new Error(`Http error! Status: ${res.status}`);
                }
                return res.json();
            })
            .then(data => {
                console.log('Response: ', data);
                insertToGameState(data);
                updateGameState();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}

let selectedPlayerCards = [];

function activateCards() {
    const playerCards =
        document.querySelectorAll('.player-cards .card');
    playerCards.forEach(card => {
        card.classList.add('active');
        card.addEventListener('click', selectPlayerCard);
    });
}

function selectPlayerCard(event) {
    const card = event.currentTarget;
    const imgPart = card.querySelector('img');
    const altText = imgPart.getAttribute('alt');
    selectedPlayerCards.push(altText);
    card.classList.add('selected');
}

function deactivateCards() {
    const playerCards =
        document.querySelectorAll('.player-cards .card');
    playerCards.forEach(card => {
        card.classList.remove('active', 'selected');
    });
    selectedPlayerCards = [];
    const use_cards_button =
        document.getElementById('use-cards');
    use_cards_button.removeEventListener('click',
        async () => {
            await makeAmoveRequest();
        });

    use_cards_button.removeEventListener('click',
        async () => {
            await beatTheCardsRequest();
        });
    showUserButtons()
    recreate_button()
}

async function userMove() {
    const initialState = JSON.stringify(gameState);
    let timeoutReached = false;

    const timer = new Promise((resolve) => {
        setTimeout(() => {
            timeoutReached = true;
            resolve("timeout");
        }, 120000);
    });

    const gameStateWatcher =
        new Promise((resolve) => {
        const interval = setInterval(() => {
            if (JSON.stringify(gameState) !== initialState) {
                clearInterval(interval);
                resolve("gameStateChanged");
            }
        }, 1000);
    });

    showUserButtons();

    const result =
        await Promise.race([timer, gameStateWatcher]);

    if (result === "timeout") {
        alert("Час на хід вичерпано, за вас походить ШІ");
        hideUserButtons();
        await AImove();
    } else if (result === "gameStateChanged") {
        console.log("Гравець виконав хід");
        hideUserButtons();
    }
}

function showSpecificButtons(spc_button_l) {
    const buttonList =
        document.getElementsByClassName('play-button')
    for (let i = 0; i < buttonList.length; i++) {
        if (!spc_button_l.includes(buttonList[i].id)) {
            buttonList[i].style.display = "none";
        } else {
            buttonList[i].style.display = "block";
        }
    }
}

function clearSelectedCards() {
    const playerCards =
        document.querySelectorAll('.player-cards .card');
    playerCards.forEach(card => {
        card.classList.remove('selected');
    });
    selectedPlayerCards = [];
}

function recreate_button() {
    const button =
        document.getElementById('use-cards');
    const newButton = button.cloneNode(true);
    button.parentNode.replaceChild(newButton, button);

}

async function makeAmoveRequest() {
    const selected =
        document.getElementsByClassName('selected')
    if (selected.length > 0) {
        return fetch('/game/makeAmove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({gameState, selectedPlayerCards}),
        })
            .then(res => {
                if (!res.ok) {
                    throw new Error(`Http error! Status: ${res.status}`);
                }
                return res.json();
            })
            .then(data => {
                if (data[0]) {
                    console.log('Response: ', data[1]);
                    insertToGameState(data[1]);
                    updateGameState();
                    clearSelectedCards();
                    recreate_button();
                } else {
                    alert("Цією комбінацією карт ходити не можна");
                    clearSelectedCards();
                }

            }).catch(error => {
                console.error('Error:', error);
            });
    } else {
        alert("Оберіть карти, якими хочете походити")
    }
}

async function beatTheCardsRequest() {
    const selected =
        document.getElementsByClassName('selected')
    if (selected.length > 0) {
        return fetch('/game/beatTheCards', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({gameState, selectedPlayerCards}),
        })
            .then(res => {
                if (!res.ok) {
                    throw new Error(`Http error! Status: ${res.status}`);
                }
                return res.json();
            })
            .then(data => {
                if (data[0]) {
                    console.log('Response: ', data[1]);
                    insertToGameState(data[1]);
                    updateGameState();
                    clearSelectedCards();
                    recreate_button();
                } else {
                    alert("Цією комбінацією карт " +
                        "ви не можете побити карти суперника");
                    clearSelectedCards();
                }

            }).catch(error => {
                console.error('Error:', error);
            });
    } else {
        alert("Оберіть карти, якими хочете походити")
    }
}

async function moveCardsRequest() {
    const selected =
        document.getElementsByClassName('selected')
    if (selected.length > 0) {
        return fetch('/game/moveTheCards', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({gameState, selectedPlayerCards}),
        })
            .then(res => {
                if (!res.ok) {
                    throw new Error(`Http error! Status: ${res.status}`);
                }
                return res.json();
            })
            .then(data => {
                if (data[0]) {
                    console.log('Response: ', data[1]);
                    insertToGameState(data[1]);
                    updateGameState();
                    clearSelectedCards();
                    recreate_button();
                } else {
                    alert("Цією комбінацією карт " +
                        "ви не можете перевести карти суперника");
                    clearSelectedCards();
                }

            }).catch(error => {
                console.error('Error:', error);
            });
    } else {
        alert("Оберіть карти, якими хочете перевести карти суперника")
    }
}


async function startGame() {
    console.log("Гра починається!");
    let i = 1;
    while (checkForWinner() === null) {
        let winner = checkForWinner();
        if (winner) {
            console.log(`Переможець ${winner}!`);
            break;
        }

        let playerNum = gameState.current_player;

        if (playerNum !== 3) {
            await AImove();
        } else {
            await userMove();
        }
        showChanges();

        i++;
    }
    window.location.href = `/victory?winner=${checkForWinner()}`;


}


document.addEventListener('DOMContentLoaded',
    async () => {
    await showLoadingScreen();
});


async function makeAmove() {
    let cardsInGame = gameState.cards_in_game;
    if (cardsInGame.length === 0) {
        activateCards();
        showSpecificButtons([USE_CARDS, DEACTIVATE_CARDS]);
        const use_cards_button =
            document.getElementById('use-cards');
        use_cards_button.addEventListener('click',
            async () => {
                await makeAmoveRequest();
            });
    }
}

async function beatTheCards() {
    let cardsInGame = gameState.cards_in_game;
    if (cardsInGame.length !== 0) {
        activateCards()
        showSpecificButtons([USE_CARDS, DEACTIVATE_CARDS]);
        const use_cards_button =
            document.getElementById('use-cards');
        use_cards_button.addEventListener('click',
            async () => {
                await beatTheCardsRequest();
            });
    }
}

async function moveCards() {
    let cardsInGame = gameState.cards_in_game;
    if (cardsInGame.length !== 0) {
        activateCards()
        showSpecificButtons([USE_CARDS, DEACTIVATE_CARDS]);
        const use_cards_button =
            document.getElementById('use-cards');
        use_cards_button.addEventListener('click',
            async () => {
                await moveCardsRequest();
            });
    }
}
