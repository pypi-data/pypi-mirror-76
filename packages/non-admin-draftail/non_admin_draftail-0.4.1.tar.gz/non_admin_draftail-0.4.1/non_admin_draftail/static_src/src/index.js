import * as Draftail from "draftail";
import draftail, {
  Link, EmbedBlock
} from "./components/Draftail/index";

import "draft-js/dist/Draft.css";
import "draftail/dist/draftail.css";
import "./styles/icons.scss";
import "./styles/styles.scss";
import {LinkSource} from "./sources/LinkSource/index";
import {EmbedSource} from "./sources/EmbedSource/index";

/**
 * Entry point loaded when the Draftail editor is in use.
 */

// Expose Draftail package as a global.
window.Draftail = Draftail;

// Expose module as a global.
window.draftail = draftail;

// Plugins for the built-in entities.
const plugins = [
  {
    type: "LINK",
    source: LinkSource,
    decorator: Link
  },
  {
    type: "EMBED",
    source: EmbedSource,
    block: EmbedBlock
  }
];

plugins.forEach(draftail.registerPlugin);
