import Wretch from "wretch";
import { CoursesResponse, CourseReponse, TermsResponse } from "./responses";

const API_URL = process.env.REACT_APP_API_URL || "";

const client = Wretch()
  .url(API_URL);

export function getTerms(): Promise<TermsResponse> {
  return client
    .url("/terms")
    .get()
    .json();
}

export function getCourses(term: string): Promise<CoursesResponse> {
  return client
    .url(`/terms/${term}`)
    .get()
    .json();
}

export function getCourse(term: string, course: string): Promise<CourseReponse> {
  return client
    .url(`/terms/${term}/${course}`)
    .get()
    .json();
}

export function postSubmission(captcha: string, email: string, sections: string[]) {
  return client
    .url('/submit')
    .post({
      captcha,
      email,
      sections,
    })
    .json();
}