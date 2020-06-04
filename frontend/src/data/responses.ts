export interface BaseResponse {
    error?: string;
    data?: any;
}

export interface TermsResponse extends BaseResponse {
    data: string[];
}

export interface CoursesResponse extends BaseResponse {
    data: CourseMap;
}

export interface CourseReponse extends BaseResponse {
    data: Course;
}

export interface CourseMap {
    [key: string]: string;
}

export interface Course {
    components: CourseComponentMap;
    name: string;
}

export interface CourseComponentMap {
    [key: string]: CourseComponent;
}

export interface CourseComponent {
    cmp_type: string;
    filled: number;
    maximum: number;
    section: string;
    status: string;
    times: string;
    type: string;
}