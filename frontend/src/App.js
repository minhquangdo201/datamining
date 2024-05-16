import * as Icon from 'react-bootstrap-icons';
import React, { useState } from 'react';
import './App.css';
import logo from './assets/spamzz.png';
import { predict, getHistory } from './appService';
const App = () => {

  const [history, setHistory] = useState([]);
  const [message, setMessage] = useState('');
  const [model, setModel] = useState('');
  const [showModal, setShowModal] = React.useState(false);
  const handleGetHistory = async () => {
    setShowModal(true);
    const response = await getHistory();
    console.log(response);
    setHistory(response);
  }

  const getModelName = (model) => {
    switch (model) {
      case 'naive bayes':
        return 'Naive Bayes';
      case 'svm':
        return 'SVM';
      case 'backpropagation':
        return 'Backpropagation';
    }
  }

  const handleChangeModel = (event) => {
    setModel(event.target.value);
  }

  const handleCheck = async (event) => {
    event.preventDefault();
    const data = {
      message: message,
      model: model
    }
    if (!data.message || !data.model || data.message === '' || data.model === '') {
      alert('Please fill all fields');
      return;
    } else {
      const response = await predict(data);
      if (response) {
        console.log(response);
        if (response.prediction === "spam") {
          alert("SPAM ALERT! This is a spam message")
          return;
        } 
        if(response.prediction === "ham") {
          alert("NO SPAM! This is not a spam message")
          return;
        }
        else {
          alert("Something went wrong!")
        }
      }
    }
  }

  return (
    <div className='flex justify-center'>
      <div className='xl:w-4/12 sm:w-10/12 form-outer shadow rounded-lg mt-10'>
        <div className='flex justify-center'>
          <img src={logo} alt='logo' className='xl:w-7/12 sm:w-8/12' />
        </div>
        <form className='px-6 pb-8'>
          <div>
            <label for="message" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your message</label>
            <textarea onChange={(e) => setMessage(e.target.value)} id="message" rows="4" className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Enter your message"></textarea>
          </div>
          <div className='flex justify-between my-3'>
            <div>
              <select value={model} onChange={handleChangeModel} className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                <option selected value="">Choose a model</option>
                <option value="naive bayes">Naive Bayes</option>
                <option value="svm">SVM</option>
                <option value="backpropagation">Backpropagation</option>
              </select>
            </div>
            <button onClick={() => handleGetHistory()} data-modal-target="default-modal" data-modal-toggle="default-modal" className="history flex items-center text-base block text-white" type="button">
              <Icon.ArrowCounterclockwise></Icon.ArrowCounterclockwise>
              <span>History</span>
            </button>
          </div>
          <div>
            <button onClick={handleCheck} type="submit" className="block w-full p-3 text-sm font-medium text-white bg-orange-500 rounded-lg focus:outline-none focus:ring focus:ring-orange-500 focus:ring-offset-2 hover:bg-orange-600">Check</button>
          </div>
        </form></div>

      {showModal ? (
        <>
          <div className="overflow-y-auto justify-center flex overflow-x-hidden mt-12 fixed inset-0 z-50 outline-none focus:outline-none">
            <div className="relative w-auto sm:w-10/12 xl:w-8/12">
              {/*content*/}
              <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                {/*header*/}
                <div className="flex items-start justify-between p-5 border-b border-solid border-blueGray-200 rounded-t">
                  <h3 className="text-3xl font-semibold">
                    History
                  </h3>
                  <button
                    className="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"
                    onClick={() => setShowModal(false)}
                  >
                    <span className="bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none">×</span>
                  </button>
                </div>
                {/*body*/}
                <div className="relative p-6 flex-auto overflow-y-auto max-h-60 ">
                  <table className='table-auto w-full text-base text-left rtl:text-right text-black dark:text-black'>
                    <thead className='text-xs text-gray-700 uppercase'>
                      <tr>
                        <th className="w-1/12 align-top">Id</th>
                        <th className="w-7/12 align-top">SMS</th>
                        <th className="w-1/12 align-top">Label</th>
                        <th className="w-1/12 align-top">Model</th>
                      </tr>
                    </thead>
                    <tbody>
                      {history.map((item, index) => (
                        <tr className='bg-white border-b hover:bg-gray-200' key={index}>
                          <td className=' align-top'>{index + 1}</td>
                          <td className="break-word align-top font-semibold">{item.message}</td>
                          {item.label === "ham" ? <td className='align-top text-green-600 font-bold'>{item.label}</td> : <td className='align-top text-red-600 font-bold'>{item.label}</td>}
                          <td className='align-top'>{getModelName(item.model)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                {/*footer*/}
                <div className="flex items-center justify-end p-6 border-t border-solid border-blueGray-200 rounded-b">
                  <button
                    className="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                    type="button"
                    onClick={() => setShowModal(false)}
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="opacity-25 fixed inset-0 z-40 bg-black"></div>
        </>
      ) : null}
    </div>
  )
}

export default App;
