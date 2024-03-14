import * as React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

export default function SuggestionCard(props: {
  text: string;
  updateValue: Function;
}) {
  return (
    <>
      <Card
        sx={{ width: 0.98 / 3, height: 1 / 4, cursor: "pointer" }}
        onClick={() => props.updateValue(props.text)}
      >
        <CardContent>
          <Typography
            sx={{ fontSize: 15, textAlign: "start" }}
            color="text.secondary"
            gutterBottom
          >
            {props.text}
          </Typography>
        </CardContent>
      </Card>
    </>
  );
}
