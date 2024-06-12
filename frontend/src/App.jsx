import Router from "./Router";
import { ThemeProvider } from "styled-components";
import GlobalStyle from "./styles/globalStyles";
import {theme} from "./styles/themes/default";

function App() {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <Router />
    </ThemeProvider>
  );
}

export default App;
