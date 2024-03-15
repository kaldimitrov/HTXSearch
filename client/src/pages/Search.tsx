import React, { useEffect, useState } from "react";
import SearchBar from "../components/SearchBar";
import "../styles/search.css";
import { ThemeProvider, createTheme, useTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { Box, IconButton } from "@mui/material";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import { grey } from "@mui/material/colors";
import InputField from "../components/InputField";
import { fetchInformation } from "../services/Requests";
import { useLocation } from "react-router-dom";

const ColorModeContext = React.createContext({ toggleColorMode: () => {} });

function SwitchTheme() {
  const theme = useTheme();
  const colorMode = React.useContext(ColorModeContext);
  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "right",
        justifyContent: "right",
        bgcolor: "background.default",
        color: "text.primary",
        borderRadius: 1,
      }}
    >
      <IconButton
        sx={{ ml: 1 }}
        onClick={colorMode.toggleColorMode}
        color="inherit"
      >
        {theme.palette.mode === "dark" ? (
          <Brightness7Icon
            sx={{
              color: "#FF1A16",
              fontSize: "35px",
            }}
          />
        ) : (
          <Brightness4Icon
            sx={{
              color: "#FF1A16",
              fontSize: "35px",
            }}
          />
        )}
      </IconButton>
    </Box>
  );
}

function Search() {
  const [mode, setMode] = useState<"light" | "dark">(
    (localStorage.getItem("theme") as "light" | "dark") || "dark"
  );
  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        localStorage.setItem("theme", mode === "light" ? "dark" : "light");
        setMode((prevMode) => (prevMode === "light" ? "dark" : "light"));
      },
    }),
    [mode]
  );
  const [input, setInput] = useState("");
  const location = useLocation();

  function updateValue(e: string) {
    setInput(e);
  }

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const queryValue = urlParams.get("query");

    setInput(queryValue || "");
    fetchInformation(queryValue as string);
  }, [location]);

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

          <div className="header">
            <div className="upload-button">
              <InputField theme={mode} />
            </div>
            <div className="title">
              <a className="text" href="/">
                HTXSearch
              </a>
            </div>
            <div className="theme">
              <SwitchTheme />
            </div>
          </div>
          <div className="main">
            <div className="search-bar">
              <SearchBar input={input} updateValue={updateValue} />
            </div>
          </div>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default Search;
