import React from 'react';
import ReactDOM from 'react-dom';


/**
 * Renders the main app page
 * on button press, gets user input and sends POST request with input data in JSON
 * recieves POST response with JSON data and renders it 
 * 
 * 
 * @module JSON5      used for parsing steps data
 *  
 * @return  {HTML}    Renders main page
 */
function App() {

    /**
     * calling async function on submit 
     * 
     * @async   Async since we need to wait for data in fetch
     */
    const handleSubmit = async(event) => {
        event.preventDefault();           // prevents reloading of page
        const formData = event.target;    // storing data from form inputs

        // converting form data to JSON for sending to backend
        const jsonData = {
          type: formData['type'].value, 
          mins: formData['mins'].value, 
          step: formData['steps'].value, 
          ingr: formData['ingredients'].value};
          
        const sendData = jsonData;          //  JSON object for sending data


        /**
         * using fetch to send JSON to api by POST method and wait for reponse
         * then rendering the recieved JSON reponse
         * 
         * @constant {JSON} showData  stores data to be diplayed
         */
        await fetch("/api/rec", {method: "POST", headers: {'Content-Type' : 'application/json'}, body: JSON.stringify(sendData)})
          .then((response) => response.json()     // storing api response
            .then((responseData) => {             // storing JSON object from api respone

              const showData = responseData;

              // for (no recipe found) error response
              if (showData.error === 1) {
                const Display = <p>No results found, please change filters</p>
                ReactDOM.render(Display,document.querySelector('#root'));
              } 


              var temp;     // used as temp storage

              /**
              * getting string of ingredients and making a JSON array
              * replacing single quotes with double for parse()
              * normal parse() is used since ingredients data has no random single quotes
              * @constant {array} ingr     stores ingredients
              */
              temp = showData.ingredients[0].replace(/'/g, '"');
              const ingr = JSON.parse(temp);


              /**
              * using JSON5 to make JSON array from string without having issues with single quotes
              * @module JSON5       better parse()
              * @constant {array} step     stores steps
              */
              const JSON5 = require('json5');
              const step = JSON5.parse(showData.steps[0]);
              // old parse() without JSON5 
              // temp = showData.steps[0].replace(/'/g, '"');
              // const step = JSON.parse(temp);


              /**
              * getting string of nutrition data and making a JSON array of numbers
              * @constant {array} nutrition    stores nutrition data
              */
              temp = showData.nutrition[0].replace('[', ' ');
              temp = temp.replace(']', '');
              temp = temp.split(',');
              const nutrition = temp;

              // Displaying recommendation output
              const Display = <React.Fragment>

                                <h1 className='rec-text-head'>{showData.name[0].toUpperCase()}</h1>

                                <p className='rec-description'>{showData.description[0].charAt(0).toUpperCase() + showData.description[0].slice(1)}</p>

                                <p className='rec-time'><b>Time to make - </b>{showData.minutes[0]} minutes</p>

                                <div class="grid-container rec-ing-steps">
                                <div>
                                <h4 className='rec-ing-text'>Ingredients -</h4>
                                <ul className='ingr_list rec-ing'>
                                  {ingr.map(item => {return <li>{item}</li>;})}
                                </ul>
                                </div>

                                <div>
                                <h4 className= 'rec-steps-text'>Steps -</h4>
                                <ol className='rec-steps'>
                                  {step.map(item => {return <li>{item}</li>;})}
                                </ol>
                                </div>
                                </div>

                                <br></br>
                                <h4 className='rec-nutri-text'>Nutritional Information -</h4>
                                <p>This recipe has {nutrition[0]} Calories</p>
                                <ul className='nutri'>
                                  <li>Total Fat = {parseInt(nutrition[1])} % DV</li>
                                  <li>Sugar = {parseInt(nutrition[2])} % DV</li>
                                  <li>Sodium = {parseInt(nutrition[3])} % DV</li>
                                  <li>Protein = {parseInt(nutrition[4])} % DV</li>
                                  <li>Saturated Fat = {parseInt(nutrition[5])} % DV</li>
                                  <li>Carbohydrates = {parseInt(nutrition[6])} % DV</li>
                                  <span><i>* % DV stands for Percent Daily Value</i></span>
                                </ul>

                              </React.Fragment>;

              ReactDOM.render(Display,document.querySelector('#root'));     // renders recipe data

            })
          )
      }


    // default return of App() which renders main page
    return (
          <div >
          <div className='out-flex'>
            <div className='flex-r'>
              <h2 className='recipe-rec-text'>Recipe Recommendation System</h2>
            </div>
            
            <div className='flex-c'> 
              <form onSubmit={e => handleSubmit(e)} className='form-style'>
                <b>

              <p>Select the Type of Food you want to have:</p> 
                <select name="type">
                  <option value="Healthy">Healthy</option>
                  <option value="Veg">Veg</option>
                  <option value="Non-Veg">Non-Veg</option>
                  <option value="Veg_Dessert">Veg Dessert</option>
                  <option value="Non-Veg_Dessert">Non-Veg Dessert</option>
                </select>

                <p>How much time do you have for preparation ?</p>
                <input name='mins' type="number" placeholder='Number in Minutes' />

                <p>How many steps in the process do you prefer ?</p>
                <input name='steps' type="number" placeholder='Number' />

                <p>How many ingredients are available with you ?</p>
                <input name='ingredients' type="number" placeholder='Number' />

                <br></br><br></br>
                <button><b>Recommend</b></button>
                <br></br><br></br>

                </b>
              </form>
            </div>
            </div>
          </div>
      )
    }

export default App;
