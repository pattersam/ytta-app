export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IVideo {
    title: string;
    description?: string;
    url: string;
    status?: string;
    id: number;
}

export interface ILabelOccurance {
    label_name: string;
    num_videos: number;
    num_occurances: number;
    avg_confidence: number;
}
