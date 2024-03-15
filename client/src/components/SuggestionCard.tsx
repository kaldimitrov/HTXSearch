import { Box, CardActions } from "@mui/material";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { useState } from "react";
import DrawIcon from "@mui/icons-material/Draw";
import { grey } from "@mui/material/colors";

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
          cursor: "pointer",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          borderRadius: 3,
          boxShadow: 3,
          "&:hover": {
            transition: "background-color 0.5s",
            backgroundColor: props.theme == "light" ? "#FFAE00" : "#FF1A16",
          },
        }}
        onClick={() => props.updateValue(props.text)}
      >
        <CardContent
          sx={{ paddingBottom: 0, paddingRight: "1rem", height: "100%" }}
        >
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
            height: "4rem",
            display: "flex",
            paddingRight: "0.5rem",
            alignItems: "end",
            justifyContent: "end",
          }}
        >
          <Box
            sx={{
              height: "2.5rem",
              width: "2.5rem",
              borderRadius: "50%",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              bgcolor: props.theme == "light" ? grey[300] : grey[900],
            }}
          >
            <DrawIcon
              sx={{
                height: "2rem",
                width: "2rem",
              }}
            />
          </Box>
        </CardActions>
      </Card>
    </>
  );
}
