import React from "react";
import SearchBar from "./components/SearchBar";
import "./App.css";
import { ThemeProvider, createTheme, useTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { Box, IconButton } from "@mui/material";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import { grey } from "@mui/material/colors";
import SuggestionCard from "./components/SuggestionCard";

const ColorModeContext = React.createContext({ toggleColorMode: () => {} });

function SwitchTheme() {
  const theme = useTheme();
  const colorMode = React.useContext(ColorModeContext);
  return (
    <Box
      sx={{
        display: "flex",
        width: "100%",
        alignItems: "right",
        justifyContent: "right",
        bgcolor: "background.default",
        color: "text.primary",
        borderRadius: 1,
        p: 3,
      }}
    >
      <IconButton
        sx={{ ml: 1 }}
        onClick={colorMode.toggleColorMode}
        color="inherit"
      >
        {theme.palette.mode === "dark" ? (
          <Brightness7Icon />
        ) : (
          <Brightness4Icon />
        )}
      </IconButton>
    </Box>
  );
}

function App() {
  const [mode, setMode] = React.useState<"light" | "dark">(
    (localStorage.getItem("theme") as "light" | "dark") || "dark"
  );
  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        localStorage.setItem("theme", mode === "light" ? "dark" : "light");
        setMode((prevMode) => (prevMode === "light" ? "dark" : "light"));
      },
    }),
    []
  );

  const [input, setInput] = React.useState("");

  function updateValue(e: string) {
    setInput(e);
  }

  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          ...(mode === "light"
            ? {
                primary: grey,
                divider: grey[200],
                text: {
                  primary: grey[900],
                  secondary: grey[900],
                },
              }
            : {
                primary: grey,
                divider: grey[200],
                background: {
                  default: grey[900],
                  paper: grey[900],
                },
                text: {
                  primary: grey[300],
                  secondary: grey[300],
                },
              }),
        },
      }),
    [mode]
  );

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <div className="body">
          <CssBaseline />

          <div className="switch-theme">
            <SwitchTheme />
          </div>
          <div className="text">
            <h1>HTXSearch</h1>
          </div>
          <div className="search-bar">
            <SearchBar input={input} updateValue={updateValue} />
            <div className="cards">
              <SuggestionCard
                text="R0 register ESP32"
                updateValue={updateValue}
                theme={mode}
              />
              <SuggestionCard
                text="STM32 information"
                updateValue={updateValue}
                theme={mode}
              />
              <SuggestionCard
                text="Timers in esp32"
                updateValue={updateValue}
                theme={mode}
              />
            </div>
          </div>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;
