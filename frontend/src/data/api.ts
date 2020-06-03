import Wretch from "wretch";

const client = Wretch();

export function getTerms() {
  return client
    .url("/terms")
    .get()
    .json();
}