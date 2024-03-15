import Paper from "@mui/material/Paper";
import SearchIcon from "@mui/icons-material/Search";
import InputBase from "@mui/material/InputBase";
import IconButton from "@mui/material/IconButton";
import { fetchInformation } from "../services/Requests";

export default function SearchBar(props: { updateValue: any; input: string }) {
  return (
    <>
      <Paper
        component="form"
        sx={{
          p: "4px 4px",
          display: "flex",
          alignItems: "center",
          borderRadius: 3,
          boxShadow: 3,
        }}
      >
        <InputBase
          sx={{ ml: 1, flex: 1, padding: 1 }}
          placeholder="Search"
          value={props.input}
          onKeyDown={async (e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              await fetchInformation(props.input);
            }
          }}
          onInput={(e: any) => {
            props.updateValue(e.target.data);
          }}
          inputProps={{ "aria-label": "search" }}
        />
        <IconButton
          type="button"
          sx={{ p: "10px" }}
          aria-label="search"
          onClick={async () => {
            await fetchInformation(props.input);
          }}
        >
          <SearchIcon />
        </IconButton>
      </Paper>
    </>
  );
}
