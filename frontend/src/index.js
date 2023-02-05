import React from 'react';
import ReactDOM from 'react-dom/client';
import { RecoilRoot } from "recoil";                  // 상태관리 라이브러리
import { BrowserRouter } from "react-router-dom";     // 라우팅 기능 라이브러리
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RecoilRoot>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </RecoilRoot>
  </React.StrictMode>
);
reportWebVitals();
