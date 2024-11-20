use std::iter::repeat;
use std::sync::Arc;
use std::time::Duration;

use eframe::emath::Vec2;
use egui::{
    Align, Frame, Label, Layout, Rect, RichText, Rounding, ScrollArea, Shape, Stroke, Ui,
    UiBuilder, Widget,
};

use hello_egui::animation::animate_continuous;
use hello_egui::inbox::UiInbox;
use hello_egui::infinite_scroll::InfiniteScroll;

use crate::demo_area;
use crate::example::{Example, ExampleTrait};
use crate::futures::{sleep, spawn};
use crate::shared_state::SharedState;

pub const CHAT_EXAMPLE: Example = Example {
    name: "Chat",
    slug: "chat",
    get: || Box::new(ChatExample::new()),
};

#[derive(Debug)]
struct HistoryLoader {
    history: Vec<ChatMessage>,
    messages: Vec<(ChatMessage, Duration)>,
}

impl HistoryLoader {
    pub fn new() -> Self {
        // let history: Vec<_> = CHAT_HISTORY
        //     .lines()
        //     .filter(|line| !line.is_empty())
        //     .map(|line| {
        //         let (name, content) = line.split_once(": ").unwrap();

        //         ChatMessage {
        //             content: content.to_string(),
        //             from: if name == "me" {
        //                 None
        //             } else {
        //                 Some(name.to_string())
        //             },
        //         }
        //     })
        //     .rev()
        //     .collect();

        // Repeat the history 5 times to make it longer.
        // let history = repeat(history)
        //     .take(5)
        //     .flat_map(|history| history.clone())
        //     .collect();

        let history = vec![];

        let messages = vec![
            (
                ChatMessage {
                    content: "안녕하세요".to_string(),
                    from: Some("me".to_string()),
                },
                Duration::from_secs_f32(0.5),
            )
        ];
        // let messages= CHAT_MESSAGES
        //         .lines()
        //         .filter(|line| !line.is_empty())
        //         .map(|line| {
        //             let (name, content) = line.split_once(": ").unwrap();

        //             let (name, duration) = name.split_once(", ").unwrap();

        //             let duration = Duration::from_secs_f32(duration.parse::<f32>().unwrap());

        //             (
        //                 ChatMessage {
        //                     content: content.to_string(),
        //                     from: if name == "me" {
        //                         None
        //                     } else {
        //                         Some(name.to_string())
        //                     },
        //                 },
        //                 duration,
        //             )
        //         })
        //         .collect(),

        Self {
            history,
            messages
        }
    }

    pub async fn load(&self, page: Option<usize>) -> (Vec<ChatMessage>, Option<usize>) {
        let page = page.unwrap_or(0);
        sleep(Duration::from_secs_f32(0.7)).await;
        let page_size = 10;
        let start = page * page_size;
        let end = usize::min(start + page_size, self.history.len());
        let has_more = end < self.history.len();
        let messages = self.history[start..end].iter().cloned().rev().collect();
        (messages, if has_more { Some(page + 1) } else { None })
    }
}

#[derive(Debug, Clone)]
pub struct ChatMessage {
    pub content: String,
    pub from: Option<String>,
}

#[derive(Debug)]
pub struct ChatExample {
    messages: InfiniteScroll<ChatMessage, usize>,
    inbox: UiInbox<ChatMessage>,
    history_loader: Arc<HistoryLoader>,
    shown: bool,
    msgs_received: usize,
    input_text: String,  // 새로 추가
}

impl ChatExample {
    pub fn new() -> Self {
        let history_loader = Arc::new(HistoryLoader::new());
        let history_loader_clone = history_loader.clone();
        let inbox = UiInbox::new();

        ChatExample {
            messages: InfiniteScroll::new().start_loader(move |cursor, cb| {
                println!("Loading messages...");
                let history_loader = history_loader_clone.clone();
                spawn(async move {
                    let (messages, cursor) = history_loader.load(cursor).await;
                    cb(Ok((messages, cursor)));
                });
            }),
            inbox,
            history_loader,
            shown: false,
            msgs_received: 0,
            input_text: String::new(),  // 새로 추가
        }
    }

    #[allow(clippy::too_many_lines)] // It's an example
    pub fn ui(&mut self, ui: &mut Ui, shared_state: &SharedState) {
        if !self.shown {
            self.shown = true;

            let tx = self.inbox.sender();
            self.history_loader
                .messages
                .iter()
                .for_each(|(message, duration)| {
                    let tx = tx.clone();
                    let duration = *duration;
                    let message = message.clone();
                    spawn(async move {
                        sleep(duration).await;
                        tx.send(message).ok();
                    });
                });
        }

        self.inbox.read(ui).for_each(|message| {
            self.messages.items.push(message);
            self.msgs_received += 1;
        });

        let title = "Chat";
        demo_area(ui, title, 200.0, |ui| {
            ScrollArea::vertical()
                .animated(false)
                .max_height(800.0)
                .auto_shrink([false, false])
                .stick_to_bottom(true)
                .show(ui, |ui| {
                    ui.set_width(ui.available_width());

                    ui.vertical_centered(|ui| {
                        if self.messages.top_loading_state().loading() {
                            ui.set_invisible();
                            ui.spinner();
                        }
                    });

                    let max_msg_width = ui.available_width() - 40.0;
                    let inner_margin = 8.0;
                    let outer_margin = 8.0;

                    self.messages.ui(ui, 5, |ui, _index, item| {
                        let is_message_from_myself = item.from.is_none();

                        // Messages from the user are right-aligned.
                        let layout = if is_message_from_myself {
                            Layout::top_down(Align::Max)
                        } else {
                            Layout::top_down(Align::Min)
                        };

                        ui.with_layout(layout, |ui| {
                            ui.set_max_width(max_msg_width);

                            let mut measure = |text| {
                                let label = Label::new(text);
                                // We need to calculate the text width here to enable the typical
                                // chat bubble layout where the own bubbles are right-aligned and
                                // the text within is left-aligned.
                                let (_pos, galley, _response) = label.layout_in_ui(
                                    &mut ui.new_child(UiBuilder::new().max_rect(ui.max_rect())),
                                );
                                let rect = galley.rect;
                                // Calculate the width of the frame based on the width of
                                // the text and add 0.1 to account for floating point errors.
                                f32::min(
                                    rect.width() + inner_margin * 2.0 + outer_margin * 2.0 + 0.1,
                                    max_msg_width,
                                )
                            };

                            let content = RichText::new(&item.content);
                            let mut msg_width = measure(content.clone());
                            let name = if let Some(from) = &item.from {
                                let name = RichText::new(from).strong();
                                let width = measure(name.clone());
                                msg_width = f32::max(msg_width, width);
                                Some(name)
                            } else {
                                None
                            };

                            // Set the width of the ui to the width of the message.
                            ui.set_min_width(msg_width);

                            let msg_color = if is_message_from_myself {
                                ui.style().visuals.widgets.inactive.bg_fill
                            } else {
                                ui.style().visuals.extreme_bg_color
                            };

                            let rounding = 8.0;
                            let margin = 8.0;
                            let response = Frame::none()
                                .rounding(Rounding {
                                    ne: if is_message_from_myself {
                                        0.0
                                    } else {
                                        rounding
                                    },
                                    nw: if is_message_from_myself {
                                        rounding
                                    } else {
                                        0.0
                                    },
                                    se: rounding,
                                    sw: rounding,
                                })
                                .inner_margin(margin)
                                .outer_margin(margin)
                                .fill(msg_color)
                                .show(ui, |ui| {
                                    ui.with_layout(Layout::top_down(Align::Min), |ui| {
                                        if let Some(from) = name {
                                            Label::new(from).ui(ui);
                                        }

                                        ui.label(&item.content);
                                    });
                                })
                                .response;

                            let points = if is_message_from_myself {
                                let top = response.rect.right_top() + Vec2::new(-margin, margin);
                                let arrow_rect =
                                    Rect::from_two_pos(top, top + Vec2::new(rounding, rounding));

                                vec![
                                    arrow_rect.left_top(),
                                    arrow_rect.right_top(),
                                    arrow_rect.left_bottom(),
                                ]
                            } else {
                                let top = response.rect.left_top() + Vec2::splat(margin);
                                let arrow_rect =
                                    Rect::from_two_pos(top, top + Vec2::new(-rounding, rounding));

                                vec![
                                    arrow_rect.left_top(),
                                    arrow_rect.right_top(),
                                    arrow_rect.right_bottom(),
                                ]
                            };

                            ui.painter()
                                .add(Shape::convex_polygon(points, msg_color, Stroke::NONE))
                        });
                    });

                    if self.msgs_received < self.history_loader.messages.len()
                        && !self.messages.initial_loading()
                    {
                        Frame::none()
                            .rounding(8.0)
                            .inner_margin(8.0)
                            .outer_margin(8.0)
                            .fill(ui.style().visuals.faint_bg_color)
                            .show(ui, |ui| {
                                ui.horizontal_top(|ui| {
                                    let mut dot = |offset| {
                                        let t = animate_continuous(
                                            ui,
                                            hello_egui::animation::easing::sine_in_out,
                                            Duration::from_secs_f32(1.0),
                                            offset,
                                        );

                                        let res = ui.allocate_response(
                                            Vec2::splat(4.0),
                                            egui::Sense::hover(),
                                        );

                                        ui.painter().circle_filled(
                                            res.rect.center() + Vec2::Y * t * 4.0,
                                            res.rect.width() / 2.0,
                                            ui.style().visuals.text_color(),
                                        )
                                    };

                                    dot(0.0);
                                    dot(0.3);
                                    dot(8.6);
                                });
                            });
                    }
                });

            ui.add_space(8.0);
            ui.horizontal(|ui| {
                let text_edit = egui::TextEdit::singleline(&mut self.input_text)
                    .hint_text("메시지를 입력하세요...")
                    .desired_width(ui.available_width() - 60.0)
                    .id("chat_input".into()); // 고유 ID 추가
                    
                let text_edit_response = ui.add(text_edit);
                
                // 메시지 전송 후나 포커스를 잃었을 때 자동으로 포커스 요청
                if text_edit_response.lost_focus() {
                    text_edit_response.request_focus();
                }
                
                if ui.button("전송").clicked() || 
                   (ui.input(|i| i.key_pressed(egui::Key::Enter))) {
                    if !self.input_text.trim().is_empty() {
                        let new_message = ChatMessage {
                            content: self.input_text.clone(),
                            from: None,
                        };
                        self.messages.items.push(new_message);
                        self.input_text.clear();
                    }
                }
            });
            ui.add_space(8.0);
        });
    }
}

impl ExampleTrait for ChatExample {
    fn ui(&mut self, ui: &mut Ui, shared_state: &mut SharedState) {
        self.ui(ui, shared_state);
    }
}