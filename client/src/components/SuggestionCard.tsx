import { CardActions } from "@mui/material";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { useState } from "react";
import DrawIcon from "@mui/icons-material/Draw";

function getWindowDimensions() {
  const { innerWidth: width, innerHeight: height } = window;
  return {
    width,
    height,
  };
}

export default function SuggestionCard(props: {
  text: string;
  updateValue: Function;
  theme: string;
}) {
  const [windowDimensions, setWindowDimensions] = useState(
    getWindowDimensions()
  );
  return (
    <>
      <Card
        sx={{
          width: windowDimensions.width > 1024 ? 0.98 / 3 : 1,
          minWidth: "16rem",
          height: 1 / 4,
          cursor: "pointer",
          borderRadius: 3,
          boxShadow: 3,
          "&:hover": {
            transition: "background-color 0.5s",
            backgroundColor: props.theme == "light" ? "#FFAE00" : "#FF1A16",
          },
        }}
        onClick={() => props.updateValue(props.text)}
      >
        <CardContent>
          <Typography
            sx={{ fontSize: "1.25rem", textAlign: "start" }}
            color="text.secondary"
            gutterBottom
          >
            {props.text}
          </Typography>
        </CardContent>
        <CardActions
          sx={{
            display: "flex",
            alignItems: "start",
            justifyContent: "end",
          }}
        >
          <DrawIcon sx={{ height: "1.5rem", width: "1.5rem" }} />
        </CardActions>
      </Card>
    </>
  );
}
