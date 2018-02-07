$(document).ready(function() {
    $('.select-subject-teacher').select2({
        placeholder: "Выберите преподавателя",
        allowClear: true
    });
    $('.select-course-number').select2({
        placeholder: "Выберите номер курса",
        allowClear: true
    });
    $('.select-course-number-subejcts').select2({
        placeholder: "Выберите предметы для текущего курса",
        allowClear: true
    });
    $('.select-schedule-group').select2({
        placeholder: "Выберите группу для которой нужно изменить расписание",
        allowClear: true
    });
    $('.select-schedule-group-alert').select2({
        placeholder: "Выберите группу которую нужно оповестить",
        allowClear: true
    });
});
