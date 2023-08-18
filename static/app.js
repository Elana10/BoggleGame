document.addEventListener("DOMContentLoaded", function(event){

    const form = document.querySelector("#guess_form");
    form.addEventListener("submit", async function(e){
        //Stops the page from refreshing after a guess word is submitted. 
        //Then sends the value to the .py server route '/guess.'
        //The '/guess' route sends back a json object which has evaluated the guess word's validity, the new current_score (if valid word), and the new high_score (if current_score beat high score).

        e.preventDefault()
        const guessInput = document.querySelector("#guessAPI")
        const guessInputVal = guessInput.value;       
        guessInput.value = ''

        const resp = await axios.post('/guess', {guess: guessInputVal})     

        addToGuessList(guessInputVal, resp.data.results);
        updateCurrentScore(resp.data.current_score);
        updateHighScore(resp.data.high_score);
        //JSON info is sent to javascript functions to update the DOM.  
        
    })

    function addToGuessList(guessInputVal, respText){
        const guessList = document.querySelector('#visible_list')
        const newGuess = document.createElement('li')
        newGuess.innerText = guessInputVal + ' - ' + respText
        newGuess.setAttribute('class', respText)
        guessList.appendChild(newGuess)
    }

    function updateCurrentScore(score){
        const currentScore = document.querySelector("#current_score")
        currentScore.innerText = "Current Score:  " + score
    }

    function updateHighScore(HS){
        const highScore = document.querySelector("#high_score_display")
        highScore.innerText = HS
    }



    const startDiv = document.querySelector("#div-start")
    startDiv.addEventListener("click", async function(e){
        const newBoard = await axios.get('/game')

        updateCurrentScore(newBoard.data.current_score)
        makeNewBoard(newBoard.data.board)
        showAttemptNum(newBoard.data.count)
        updateHighScore(newBoard.data.high_score)
        showGuessForm()
        clearOutGuessList()
        countDown()
       
    })

    function makeNewBoard(board){
        const board1 = document.getElementById('div-table')
        const table1 = document.getElementById('table-table')
        board1.removeChild(table1)
        
        const table = document.createElement('table')
        table.setAttribute('id', 'table-table')

        for(rowData of board){
            const rowNew = document.createElement('tr')
            for(ltr of rowData){
                const square = document.createElement('td')
                square.innerText = ltr
                rowNew.append(square)
            }

            table.append(rowNew)
        }

        board1.append(table)
    }

    function showAttemptNum(count){
        const attemptNum = document.getElementById('attempt_num')
        attemptNum.innerText = count
    }

    function clearOutGuessList(){
        const visualList = document.getElementById('visible_list')

        while (visualList.firstChild){
            visualList.removeChild(visualList.firstChild)
        }
    }

    function countDown(){

        let remainingSeconds = 60;

        const timerCount = setInterval(function(){
            const timerBox = document.getElementById('timer');
            timerBox.innerText = remainingSeconds;

            remainingSeconds --;

            if (remainingSeconds < 0){
                clearInterval(timerCount);
                const guessForm = document.getElementById('guess_form')
                guessForm.setAttribute('class', 'hide')
                

            }

        }, 1000)

    }

    function showGuessForm(){
        const guessForm = document.getElementById('guess_form')
        guessForm.setAttribute('class', 'see')
    }


})

